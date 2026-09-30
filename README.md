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
