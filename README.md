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
