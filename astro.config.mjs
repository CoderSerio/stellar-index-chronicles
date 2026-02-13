// @ts-check

import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
	site: 'https://coderserio.github.io/stellar-index-chronicles/',
	base: '/stellar-index-chronicles/',
	integrations: [mdx(), sitemap()],
});
