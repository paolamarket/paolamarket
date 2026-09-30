#!/usr/bin/env python3
"""No-API auto publisher for Paola Market.
Creates one new HTML article from data/topics.json, appends it to data/posts.json,
and advances data/state.json. No paid AI service is required.
"""
from pathlib import Path
import json, re, html
from datetime import date, datetime, timedelta

ROOT=Path(__file__).resolve().parents[1]
TOPICS=ROOT/'data'/'topics.json'; POSTS=ROOT/'data'/'posts.json'; STATE=ROOT/'data'/'state.json'; OUT=ROOT/'blog'/'posts'

def slugify(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def esc(s): return html.escape(str(s))

def article_html(topic, slug):
    today=date.today().isoformat(); title=topic['title']; category=topic['category']
    if topic['kind']=='recipe':
        ingredients=''.join(f'<li>{esc(x)}</li>' for x in topic['ingredients'])
        steps=''.join(f'<li>{esc(x)}</li>' for x in topic['steps'])
        body=f'''<p>Looking for a straightforward drink you can make at home? This version keeps the method simple and the flavors balanced.</p>
        <div class="recipe-box"><h2>Ingredients</h2><ul>{ingredients}</ul><h2>Method</h2><ol>{steps}</ol><p><strong>Paola Market tip:</strong> {esc(topic.get('tip','Use fresh ingredients and serve responsibly.'))}</p></div>
        <h2>Make it your own</h2><p>Small adjustments can change the drink without making it complicated. Try a different garnish, use more or less mixer to suit your taste, and keep your ingredients cold for a cleaner finish.</p>
        <h2>Serving idea</h2><p>Serve with water and food when entertaining, and keep portions moderate so everyone can enjoy the occasion responsibly.</p>'''
    else:
        points=''.join(f'<li>{esc(x)}</li>' for x in topic['points'])
        body=f'''<p>This quick guide is designed to make shopping and serving easier without unnecessary rules. Use these ideas as a starting point and choose what fits your taste and occasion.</p>
        <h2>What to know</h2><ul>{points}</ul><h2>Keep it simple</h2><p>Personal preference matters. If you enjoy a particular style, that is often more useful than chasing a “perfect” pairing or bottle. For gatherings, offer water and nonalcoholic options as well.</p>'''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} | Paola Market</title><meta name="description" content="{esc(title)} — an approachable Paola Market guide from Paola, Kansas for adults 21+."><meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1"><meta property="og:type" content="article"><meta property="og:title" content="{esc(title)} | Paola Market"><meta property="og:description" content="{esc(title)} — an approachable guide from Paola Market in Paola, Kansas."><meta property="og:image" content="../../assets/paola-market-logo.png"><script type="application/ld+json">{{"@context":"https://schema.org","@type":"BlogPosting","headline":{json.dumps(title)},"datePublished":"{today}","dateModified":"{today}","author":{{"@type":"Organization","name":"Paola Market"}},"publisher":{{"@type":"Organization","name":"Paola Market"}},"about":{json.dumps(category)}}}</script><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet"><link rel="stylesheet" href="../../styles.css"><link rel="stylesheet" href="../blog.css"></head><body class="blog-body"><header class="blog-header"><a class="brand" href="../../"><img src="../../assets/paola-market-logo.png" alt="Paola Market"><span>Paola Market</span></a><nav><a href="../../">Home</a><a href="../">Blog</a><a href="../../#visit">Visit</a></nav></header><main class="article-main"><a class="article-back" href="../">← Back to The Paola Pour</a><article><header class="article-head"><p class="eyebrow">{esc(category)}</p><h1>{esc(title)}</h1><div class="meta">Published {today} • Paola Market</div></header><div class="article-body">{body}<div class="responsible-note"><strong>21+ only.</strong> Alcohol affects everyone differently. Please enjoy responsibly and never drink and drive.</div></div></article><img class="article-logo" src="../../assets/paola-market-logo.png" alt="Paola Market"></main></body></html>'''

def prune_old_posts(posts):
    """Delete generated blog posts older than 60 days and return the retained list.

    A post dated exactly 60 days ago is retained. It is removed starting on day 61.
    """
    cutoff = date.today() - timedelta(days=60)
    kept=[]
    removed=[]
    for post in posts:
        try:
            post_date=datetime.strptime(post.get('date',''), '%Y-%m-%d').date()
        except (TypeError, ValueError):
            # Keep malformed/legacy records rather than deleting them unexpectedly.
            kept.append(post)
            continue
        if post_date < cutoff:
            slug=post.get('slug','')
            path=OUT/f'{slug}.html'
            if slug and path.exists():
                path.unlink()
            removed.append(slug)
        else:
            kept.append(post)
    if removed:
        print(f'Removed {len(removed)} post(s) older than 60 days.')
    return kept

def main():
    topics=json.loads(TOPICS.read_text()); posts=json.loads(POSTS.read_text()); state=json.loads(STATE.read_text())
    posts=prune_old_posts(posts)
    i=state.get('next_topic_index',0)%len(topics); topic=topics[i]; slug=slugify(topic['title'])
    existing={p['slug'] for p in posts}
    if slug in existing:
        POSTS.write_text(json.dumps(posts,indent=2),encoding='utf-8'); state['next_topic_index']=(i+1)%len(topics); STATE.write_text(json.dumps(state,indent=2)); return
    OUT.mkdir(parents=True,exist_ok=True); (OUT/f'{slug}.html').write_text(article_html(topic,slug),encoding='utf-8')
    excerpt=(f"An easy {topic.get('spirit','drink')} recipe with a simple method and serving tips." if topic['kind']=='recipe' else "A practical, beginner-friendly guide with simple tips you can use right away.")
    posts.insert(0,{"slug":slug,"title":topic['title'],"category":topic['category'],"date":date.today().isoformat(),"excerpt":excerpt,"minutes":4 if topic['kind']=='recipe' else 5})
    POSTS.write_text(json.dumps(posts,indent=2),encoding='utf-8'); state['next_topic_index']=(i+1)%len(topics); STATE.write_text(json.dumps(state,indent=2),encoding='utf-8')
    print(f'Published: {topic["title"]}')
if __name__=='__main__': main()
