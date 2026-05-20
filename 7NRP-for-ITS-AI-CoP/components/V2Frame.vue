<template>
  <section class="v2-slide" :class="{ 'v2-dark': dark, 'v2-quiet': quiet }">
    <div class="v2-left-rule" />
    <header v-if="kicker || title" class="v2-header">
      <p v-if="kicker" class="v2-kicker">{{ kicker }}</p>
      <h1 v-if="title">{{ title }}</h1>
    </header>
    <main class="v2-body" :class="bodyClass">
      <slot />
    </main>
    <footer v-if="footer" class="v2-footer">
      <span>{{ footerText }}</span>
      <span v-if="page">{{ page }}</span>
    </footer>
  </section>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    kicker?: string
    title?: string
    page?: string
    dark?: boolean
    quiet?: boolean
    footer?: boolean
    footerText?: string
    bodyClass?: string
  }>(),
  {
    footer: true,
    footerText: 'NRP @ 7NRP  ·  ITS AI Community of Practice  ·  May 2026',
    bodyClass: '',
  },
)
</script>
