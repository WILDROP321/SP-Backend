# Sneak Peek — Content Utilities

**Browser-assisted image extraction for a newsletter content workflow.**

This repository contains Python utilities that use Selenium and Firefox to inspect web pages, collect image sources, and enrich article data with featured imagery.

## What it does

- Scrolls through pages to load content.
- Extracts image URLs and cleans URL formatting.
- Finds featured images for article pages.
- Processes JSON article data for a publishing workflow.

## Repository guide

- `app.py` contains browser automation, image extraction, and JSON processing.
- `test.py` contains an experimental companion script.
- `test.json` contains sample data.

**Stack:** Python, Selenium, Firefox / GeckoDriver, and JSON.

## Related work

[SP-server](https://github.com/WILDROP321/SP-server) contains the Flask publishing site for Sneak Peek.

This is an early content-processing utility. Browser setup and page selectors may require updates for the target environment and source websites.

Built by [Arya Prabhu](https://github.com/WILDROP321).
