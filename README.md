# Paola Market website

Premium animated static website for **Paola Market**, 304 Baptiste Dr, Paola, KS.

## What is included
- Responsive animated homepage
- 21+ age gate
- "Now Open" messaging
- Beer / wine / spirits sections
- Directions to the store
- Blog + cocktail recipe hub called **The Paola Pour**
- Searchable blog index
- Starter posts
- Free no-API auto-blog publisher using GitHub Actions

## Free auto-blog mode
`tools/auto_blog.py` publishes the next topic from `data/topics.json` as an HTML article and updates `data/posts.json`.

The GitHub Action in `.github/workflows/auto-blog.yml` runs once daily and commits the new post to the repository. This mode does **not** call a paid AI API.

To add more future posts, add topic objects to `data/topics.json`.

### Important distinction
A truly new article written by ChatGPT/OpenAI automatically on every scheduled run requires an API connection and API usage may have a cost. This package therefore defaults to the no-API system so the scheduled publisher itself has no AI API charge.

## Deploy on GitHub Pages
1. Upload all files to the repository root.
2. In GitHub open **Settings → Pages**.
3. Choose **Deploy from a branch**.
4. Select your main branch and `/ (root)`.
5. Save.

## Change blog schedule
Edit `.github/workflows/auto-blog.yml` and change the `cron` line.

## Store hours / phone / social links
These were not added because they were not provided. Add them once finalized.


## Auto-blog library and retention
- `data/topics.json` contains **1,000 unique blog topics**.
- The GitHub Action publishes one topic per scheduled run.
- The publisher automatically deletes generated blog HTML files and `posts.json` entries **after they are more than 60 days old**.
- A post dated exactly 60 days ago remains live; it is removed beginning on day 61.
- With one post per day, the live blog will normally contain about 60 recent auto-generated posts, plus any manually maintained posts still within the same retention window.
- The topic index keeps moving forward, so the 1,000-topic library provides roughly 2.7 years of daily topics before cycling.


## SEO / future domain setup

This version includes Google-friendly LocalBusiness/LiquorStore structured data, social metadata, crawl directives, local Paola/Miami County signals, product-category entities, blog article schema, mobile/PWA metadata, and a domain-aware sitemap generator.

**Important:** do not hide blocks of keyword-stuffed text in CSS/HTML. Google classifies hidden text and keyword stuffing as spam. This site keeps search metadata in the `<head>` and JSON-LD, where it belongs, and keeps customer-visible copy natural. Google also does not use the old `meta keywords` tag as a ranking signal; it is included only as a legacy/topic reference.

When you buy your domain, edit `data/site_config.json` and set `site_url`, for example:

```json
{
  "site_url": "https://www.yourdomain.com",
  "business_name": "Paola Market"
}
```

Then run:

```bash
python tools/seo_site.py
```

That automatically adds/updates canonical URLs, `og:url`, absolute schema URLs, `sitemap.xml`, and the Sitemap line in `robots.txt`. The daily auto-blog workflow also runs this SEO generator, so future posts are added to the sitemap automatically once the domain is configured.


## v12 competitor-inspired UX improvements
This version adds original Paola Market sections inspired by useful patterns found on strong local liquor-store websites: prominent call-ahead availability help, party/occasion guidance, Google review CTA, an FAQ section, and mobile quick-action buttons for Call / Directions / Shop. No competitor text, branding, imagery, pricing, or proprietary content is copied.


## Services added in v13
- Special orders: call-ahead requests when an item can be sourced through store distributors.
- Drive-thru service.
- Party and event orders.
- Cigars.
- Tastings section with a clearly marked easy-update HTML block.

### Updating the tasting section
Open `index.html` and search for `TASTING EVENT: EASY UPDATE AREA`. Replace only the content inside the `.tasting-event-card` block with the event name, date, time, featured product/category, and any 21+ details. When there is no scheduled tasting, leave the current placeholder card in place.

## v14 link and FAQ updates
- Added Instagram beside Facebook in the Tastings section.
- Removed the Google Review FAQ item.
- Linked the drink-recipes FAQ directly to The Paola Pour blog.
- Linked the tastings FAQ directly to the Tastings section.
- Standardized phone links to `tel:+19132834560` for mobile dialing.
- Changed every Directions/Open in Maps action to Google Maps Directions with Paola Market's destination prefilled.
