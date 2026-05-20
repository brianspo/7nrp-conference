from __future__ import annotations

import json
import re
from pathlib import Path
from zipfile import ZipFile

from lxml import etree


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}

PPTX = Path("NRP_7NRP_ITS_AI_CoP_v2.pptx")
OUT = Path("slides-data.ts")


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def hex_color(value: str | None) -> str | None:
    if not value:
        return None
    if re.fullmatch(r"[0-9A-Fa-f]{6}", value):
        return f"#{value.upper()}"
    return None


def read_color(node) -> str | None:
    if node is None:
        return None
    srgb = node.find(".//a:srgbClr", NS)
    if srgb is not None:
        return hex_color(srgb.get("val"))
    scheme = node.find(".//a:schemeClr", NS)
    if scheme is not None:
        # Theme colors used in this deck. Keep a conservative fallback for any
        # unresolved scheme color.
        return {
            "accent1": "#065A82",
            "accent2": "#1C7293",
            "accent3": "#C99B2D",
            "tx1": "#1A2233",
            "tx2": "#374151",
            "bg1": "#FFFFFF",
            "bg2": "#F4F6FA",
        }.get(scheme.get("val"), "#1A2233")
    return None


def get_xfrm(node) -> dict[str, float]:
    xfrm = node.find("./p:spPr/a:xfrm", NS)
    if xfrm is None:
        xfrm = node.find("./p:xfrm", NS)
    if xfrm is None:
        return {"x": 0, "y": 0, "w": 0, "h": 0}
    off = xfrm.find("a:off", NS)
    ext = xfrm.find("a:ext", NS)
    return {
        "x": float(off.get("x", 0)) if off is not None else 0,
        "y": float(off.get("y", 0)) if off is not None else 0,
        "w": float(ext.get("cx", 0)) if ext is not None else 0,
        "h": float(ext.get("cy", 0)) if ext is not None else 0,
    }


def pct_box(box: dict[str, float], width: float, height: float) -> dict[str, float]:
    return {
        "x": round(box["x"] / width * 100, 5),
        "y": round(box["y"] / height * 100, 5),
        "w": round(box["w"] / width * 100, 5),
        "h": round(box["h"] / height * 100, 5),
    }


def shape_kind(sp) -> str:
    geom = sp.find("./p:spPr/a:prstGeom", NS)
    prst = geom.get("prst") if geom is not None else "rect"
    return {
        "rect": "rect",
        "ellipse": "ellipse",
        "line": "line",
        "rtTriangle": "rtTriangle",
    }.get(prst, "rect")


def shape_style(sp) -> dict:
    sppr = sp.find("./p:spPr", NS)
    if sppr is None:
        return {}
    style: dict[str, object] = {}
    fill = sppr.find("./a:solidFill", NS)
    if fill is not None:
        style["fill"] = read_color(fill)
    elif sppr.find("./a:noFill", NS) is not None:
        style["fill"] = "transparent"

    line = sppr.find("./a:ln", NS)
    if line is not None:
        if line.find("./a:noFill", NS) is not None:
            style["stroke"] = "transparent"
        else:
            style["stroke"] = read_color(line.find("./a:solidFill", NS))
            if line.get("w"):
                style["strokeWidthPt"] = round(int(line.get("w")) / 12700, 2)
    return {k: v for k, v in style.items() if v is not None}


def parse_text(sp) -> dict | None:
    tx = sp.find("./p:txBody", NS)
    if tx is None:
        return None
    body = tx.find("./a:bodyPr", NS)
    paragraphs = []
    for p in tx.findall("./a:p", NS):
        ppr = p.find("./a:pPr", NS)
        align = (ppr.get("algn") if ppr is not None else None) or "l"
        runs = []
        for r in p.findall("./a:r", NS):
            text = "".join(t.text or "" for t in r.findall("./a:t", NS))
            if not text:
                continue
            rpr = r.find("./a:rPr", NS)
            run = {"text": text}
            if rpr is not None:
                if rpr.get("sz"):
                    run["fontSizePt"] = round(int(rpr.get("sz")) / 100, 2)
                if rpr.get("b") == "1":
                    run["bold"] = True
                if rpr.get("i") == "1":
                    run["italic"] = True
                if rpr.get("spc"):
                    run["letterSpacingPt"] = round(int(rpr.get("spc")) / 100, 2)
                color = read_color(rpr.find("./a:solidFill", NS))
                if color:
                    run["color"] = color
            runs.append(run)
        if runs:
            paragraphs.append({"align": align, "runs": runs})
    if not paragraphs:
        return None
    return {
        "anchor": (body.get("anchor") if body is not None else None) or "t",
        "paragraphs": paragraphs,
    }


def parse_chart(zf: ZipFile, rel_id: str, rels_path: str) -> dict | None:
    rels = etree.fromstring(zf.read(rels_path))
    target = None
    for rel in rels:
        if rel.get("Id") == rel_id:
            target = rel.get("Target")
            break
    if not target:
        return None
    chart_path = (Path(rels_path).parent / target).as_posix().replace("ppt/slides/_rels/../", "ppt/")
    chart_path = chart_path.replace("ppt/slides/charts/", "ppt/charts/")
    root = etree.fromstring(zf.read(chart_path))
    ser = root.find(".//c:doughnutChart/c:ser", NS)
    if ser is None:
        return None
    labels = [v.text or "" for v in ser.findall(".//c:cat//c:v", NS)]
    values = [float(v.text or 0) for v in ser.findall(".//c:val//c:v", NS)]
    colors = []
    for dpt in ser.findall("./c:dPt", NS):
        idx = int(dpt.find("./c:idx", NS).get("val"))
        color = read_color(dpt.find(".//c:spPr/a:solidFill", NS))
        while len(colors) <= idx:
            colors.append("#CBD5E1")
        colors[idx] = color or "#CBD5E1"
    return {
        "kind": "doughnut",
        "labels": labels,
        "values": values,
        "colors": colors,
    }


def parse_pptx() -> list[dict]:
    slides = []
    with ZipFile(PPTX) as zf:
        pres = etree.fromstring(zf.read("ppt/presentation.xml"))
        size = pres.find(".//p:sldSz", NS)
        width = float(size.get("cx"))
        height = float(size.get("cy"))
        slide_names = sorted(
            [n for n in zf.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)],
            key=lambda n: int(re.search(r"slide(\d+)", n).group(1)),
        )
        for slide_num, name in enumerate(slide_names, start=1):
            root = etree.fromstring(zf.read(name))
            bg = root.find(".//p:bg", NS)
            background = read_color(bg.find(".//a:solidFill", NS)) if bg is not None else "#FFFFFF"
            if not background:
                background = "#FFFFFF"
            sp_tree = root.find(".//p:cSld/p:spTree", NS)
            shapes = []
            for child in sp_tree:
                tag = local_name(child.tag)
                if tag == "sp":
                    box = pct_box(get_xfrm(child), width, height)
                    text = parse_text(child)
                    style = shape_style(child)
                    kind = shape_kind(child)
                    if kind == "line":
                        style.setdefault("stroke", "#CBD5E1")
                    shape = {"kind": kind, **box, **style}
                    if text:
                        shape["text"] = text
                    if shape.get("fill") or shape.get("stroke") or text or kind == "line":
                        shapes.append(shape)
                elif tag == "graphicFrame":
                    chart = child.find(".//c:chart", NS)
                    if chart is None:
                        continue
                    data = parse_chart(
                        zf,
                        chart.get(f"{{{NS['r']}}}id"),
                        f"ppt/slides/_rels/slide{slide_num}.xml.rels",
                    )
                    if data:
                        shapes.append({"kind": "chart", **pct_box(get_xfrm(child), width, height), "chart": data})
            slides.append({"id": slide_num, "background": background, "shapes": shapes})
    return slides


def main() -> None:
    slides = parse_pptx()
    OUT.write_text(
        "export const slides = "
        + json.dumps(slides, ensure_ascii=False, indent=2)
        + " as const;\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUT} with {len(slides)} slides.")


if __name__ == "__main__":
    main()
