<template>
  <section class="native-slide" :class="{ 'native-slide-dark': dark }">
    <div class="native-accent" />
    <div v-if="kicker || title" class="native-header">
      <div v-if="kicker" class="native-kicker">{{ kicker }}</div>
      <h1 v-if="title">{{ title }}</h1>
    </div>
    <div class="native-body" :class="bodyClass">
      <slot />
    </div>
    <div v-if="footer !== false" class="native-footer">
      <span>{{ footerText }}</span>
      <span v-if="page">{{ page }}</span>
    </div>
  </section>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    kicker?: string
    title?: string
    page?: string
    dark?: boolean
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
