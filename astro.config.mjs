// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

const CORE_T1 = new Set([
  'nebosh-igc-assignment-help',
  'nebosh-ngc-assignment-help',
  'nebosh-open-book-exam-obe-help',
  'nebosh-diploma-assignment-help',
  'nebosh-assignment-help-online',
]);

const CORE_T2_PROCESS = new Set([
  'nebosh-ig1-assignment-model-answers',
  'nebosh-ig2-practical-assessment-help',
  'nebosh-assignment-marking-criteria-explained',
  'how-to-pass-nebosh-assignment-first-time',
  'nebosh-assignment-word-count-requirements',
  'nebosh-assignment-referral-recovery',
]);

const CORE_T2_SPECIALIST = new Set([
  'nebosh-fire-certificate-assignment-help',
  'nebosh-environmental-certificate-assignment-help',
  'nebosh-construction-certificate-assignment-help',
  'nebosh-obe-sample-questions-worked-answers',
  'nebosh-examiner-reports-analysis',
]);

function getSlug(url) {
  return url.replace(/^https?:\/\/[^/]+\//, '').replace(/\/$/, '');
}

export default defineConfig({
  site: 'https://www.naboshassignment.help',
  integrations: [
    sitemap({
      serialize(item) {
        const slug = getSlug(item.url);

        if (slug === '') {
          item.priority = 1.0;
          item.changefreq = 'weekly';
        } else if (CORE_T1.has(slug)) {
          item.priority = 0.9;
          item.changefreq = 'weekly';
        } else if (CORE_T2_PROCESS.has(slug)) {
          item.priority = 0.8;
          item.changefreq = 'monthly';
        } else if (CORE_T2_SPECIALIST.has(slug)) {
          item.priority = 0.75;
          item.changefreq = 'monthly';
        } else {
          item.priority = 0.6;
          item.changefreq = 'monthly';
        }

        return item;
      },
    }),
  ],
});
