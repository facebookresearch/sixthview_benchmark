// Copyright (c) Meta Platforms, Inc. and affiliates.
// SPDX-License-Identifier: CC-BY-NC-4.0

module.exports = {
  title: 'SixthView Benchmark',
  tagline: 'Spatial reasoning from text and images',
  url: 'https://facebookresearch.github.io',
  baseUrl: '/sixthview_benchmark/',
  organizationName: 'facebookresearch',
  projectName: 'sixthview_benchmark',
  trailingSlash: true,
  onBrokenLinks: 'throw',
  themes: ['@docusaurus/theme-classic'],
  plugins: [
    ['@docusaurus/plugin-content-docs', {routeBasePath: '/', sidebarPath: false}],
    '@docusaurus/plugin-sitemap',
  ],
  themeConfig: {
    navbar: {
      title: 'SixthView Benchmark',
      items: [{
        href: 'https://github.com/facebookresearch/sixthview_benchmark',
        label: 'GitHub',
        position: 'right',
      }],
    },
    footer: {
      copyright: 'Copyright © Meta Platforms, Inc. and affiliates. CC BY-NC 4.0.',
    },
  },
};
