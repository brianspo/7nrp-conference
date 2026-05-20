<template>
  <section class="ppt-slide" :style="{ backgroundColor: slide.background }">
    <template v-for="(shape, index) in slide.shapes" :key="index">
      <div v-if="shape.kind === 'chart'" class="ppt-chart" :style="boxStyle(shape)">
        <div class="ppt-doughnut-wrap">
          <div class="ppt-doughnut" :style="doughnutStyle(shape.chart)" />
          <div
            v-for="(_value, idx) in shape.chart.values"
            :key="idx"
            class="ppt-slice-label"
            :style="sliceLabelStyle(shape.chart, idx)"
          >
            {{ shape.chart.values[idx] }}%
          </div>
        </div>
        <div class="ppt-chart-legend">
          <div v-for="(label, idx) in shape.chart.labels" :key="label" class="ppt-chart-row">
            <span class="ppt-swatch" :style="{ backgroundColor: shape.chart.colors[idx] }" />
            <span>{{ label }}</span>
            <strong>{{ shape.chart.values[idx] }}%</strong>
          </div>
        </div>
      </div>

      <div
        v-else
        class="ppt-shape"
        :class="shapeClasses(shape)"
        :style="shapeStyle(shape)"
      >
        <div v-if="shape.text" class="ppt-text" :style="textBoxStyle(shape.text)">
          <p
            v-for="(paragraph, pIndex) in shape.text.paragraphs"
            :key="pIndex"
            :style="{ textAlign: align(paragraph.align) }"
          >
            <span
              v-for="(run, rIndex) in paragraph.runs"
              :key="rIndex"
              :style="runStyle(run, shape)"
            >{{ run.text }}</span>
          </p>
        </div>
      </div>
    </template>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { slides } from '../slides-data'
type Run = {
  text: string
  fontSizePt?: number
  bold?: boolean
  italic?: boolean
  color?: string
  letterSpacingPt?: number
}

type Paragraph = { align?: string; runs: Run[] }
type TextBox = { anchor?: string; paragraphs: Paragraph[] }
type Chart = { labels: string[]; values: number[]; colors: string[] }
type Shape = {
  kind: string
  x: number
  y: number
  w: number
  h: number
  fill?: string
  stroke?: string
  strokeWidthPt?: number
  text?: TextBox
  chart?: Chart
}

const props = defineProps<{ index: number }>()
const slide = computed<any>(() => slides[props.index])

function boxStyle(shape: Shape) {
  return {
    left: `${shape.x}%`,
    top: `${shape.y}%`,
    width: `${shape.w}%`,
    height: `${shape.h}%`,
  }
}

function shapeStyle(shape: Shape) {
  const base: Record<string, string | number> = {
    ...boxStyle(shape),
    backgroundColor: shape.fill ?? 'transparent',
    borderColor: shape.stroke ?? 'transparent',
    borderWidth: `${shape.strokeWidthPt ?? 0}pt`,
  }

  if (shape.kind === 'line') {
    base.backgroundColor = shape.stroke ?? '#CBD5E1'
    base.height = shape.h > 0 ? `${shape.h}%` : `${Math.max(shape.strokeWidthPt ?? 1, 1)}pt`
    base.borderWidth = '0'
  }

  return base
}

function shapeClasses(shape: Shape) {
  return [
    `ppt-${shape.kind}`,
    {
      'has-text': !!shape.text,
      'ppt-transparent-text': !!shape.text && (!shape.fill || shape.fill === 'transparent'),
    },
  ]
}

function textBoxStyle(text: TextBox) {
  return {
    justifyContent:
      text.anchor === 'ctr' ? 'center' : text.anchor === 'b' ? 'flex-end' : 'flex-start',
  }
}

function align(value?: string) {
  return value === 'ctr' ? 'center' : value === 'r' ? 'right' : 'left'
}

function runStyle(run: Run, shape: Shape) {
  const pointToCqw = 0.10417
  const scale = textScale(run, shape)
  return {
    fontSize: run.fontSizePt ? `${run.fontSizePt * pointToCqw * scale}cqw` : undefined,
    fontWeight: run.bold ? 700 : 400,
    fontStyle: run.italic ? 'italic' : 'normal',
    color: run.color ?? '#1A2233',
    letterSpacing: run.letterSpacingPt ? `${run.letterSpacingPt * pointToCqw * Math.min(scale, 1.08)}cqw` : undefined,
  }
}

function textScale(run: Run, shape: Shape) {
  const text = run.text.trim()
  const size = run.fontSizePt ?? 10
  const isTransparent = !shape.fill || shape.fill === 'transparent'
  const isMetric = size >= 30 && /^[\d,.]+(?:\s?[A-Z]+)?$/.test(text)
  const isCompactStat = size >= 20 && shape.w <= 16 && /^[\d,.]+(?:\s?[A-Z%]+)?$/.test(text)
  const isProcessCardTitle =
    run.bold && run.color === '#FFFFFF' && size >= 13 && shape.w <= 18 && shape.h <= 8 && !/^\d+$/.test(text)
  const isTopTitle = shape.y < 18 && size >= 24

  if (isMetric) return 1.24
  if (isCompactStat) return 1.42
  if (isProcessCardTitle) return 1.32
  if (isTopTitle && text.length > 38) return 1.02
  if (isTopTitle) return 1.08
  if (isTransparent && run.bold && run.color === '#FFFFFF' && size >= 20 && shape.w <= 6) return 1.16
  if (isTransparent && run.bold && size >= 14) return 1.12
  if (isTransparent && run.bold && size >= 11) return 1.18
  if (isTransparent && size <= 10 && shape.w <= 30 && shape.h <= 9) return 1.16
  if (isTransparent && size <= 11) return 1.08
  return 1
}

function total(values: readonly number[] = []) {
  return values.reduce((sum, value) => sum + value, 0)
}

function doughnutStyle(chart?: Chart) {
  if (!chart) return {}
  const sum = total(chart.values) || 1
  let cursor = 0
  const stops = chart.values.map((value, index) => {
    const start = cursor
    cursor += (value / sum) * 100
    return `${chart.colors[index] ?? '#CBD5E1'} ${start}% ${cursor}%`
  })
  return { background: `conic-gradient(${stops.join(', ')})` }
}

function sliceLabelStyle(chart: Chart, index: number) {
  const sum = total(chart.values) || 1
  const before = chart.values.slice(0, index).reduce((acc, value) => acc + value, 0)
  const midpoint = ((before + chart.values[index] / 2) / sum) * 360
  const angle = (midpoint * Math.PI) / 180
  const radius = chart.values[index] < 5 ? 43 : 34
  const x = 50 + Math.sin(angle) * radius
  const y = 50 - Math.cos(angle) * radius

  return {
    left: `${x}%`,
    top: `${y}%`,
    color: readableLabelColor(chart.colors[index]),
  }
}

function readableLabelColor(color = '#000000') {
  const hex = color.replace('#', '')
  const r = parseInt(hex.slice(0, 2), 16)
  const g = parseInt(hex.slice(2, 4), 16)
  const b = parseInt(hex.slice(4, 6), 16)
  const luminance = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
  return luminance > 0.55 ? '#1A2233' : '#FFFFFF'
}
</script>
