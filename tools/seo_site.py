#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import urljoin
import json, re, html

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/'data'/'site_config.json'

def clean_url(u):
    u=(u or '').strip().rstrip('/')
    if u and not re.match(r'^https?://',u,re.I):
        u='https://'+u
    return u

def html_files():
    return [ROOT/'index.html', ROOT/'blog'/'index.html', *sorted((ROOT/'blog'/'posts').glob('*.html'))]

def public_url(path, base):
    rel=path.relative_to(ROOT).as_posix()
    if rel=='index.html': return base+'/'
    if rel.endswith('/index.html'): rel=rel[:-10]
    return base+'/'+rel

def set_link_tag(text, rel, href):
    pat=rf'<link\s+rel=["\']{re.escape(rel)}["\'][^>]*>'
    tag=f'<link rel="{rel}" href="{html.escape(href, quote=True)}">'
    if re.search(pat,text,re.I): return re.sub(pat,tag,text,count=1,flags=re.I)
    return text.replace('</head>',f'  {tag}\n</head>',1)

def set_meta_property(text, prop, content):
    pat=rf'<meta\s+property=["\']{re.escape(prop)}["\'][^>]*>'
    tag=f'<meta property="{prop}" content="{html.escape(content, quote=True)}">'
    if re.search(pat,text,re.I): return re.sub(pat,tag,text,count=1,flags=re.I)
    return text.replace('</head>',f'  {tag}\n</head>',1)

def absolutize_jsonld(text, page_url, base):
    def repl(m):
        raw=m.group(1)
        try: data=json.loads(raw)
        except Exception: return m.group(0)
        def walk(x):
            if isinstance(x,dict):
                for k,v in list(x.items()):
                    if k in {'image','logo'} and isinstance(v,str) and not re.match(r'^https?://',v):
                        x[k]=urljoin(page_url,v)
                    elif k=='@id' and isinstance(v,str) and v.startswith('#'):
                        x[k]=base+'/'+v
                    else: walk(v)
            elif isinstance(x,list):
                for y in x: walk(y)
        walk(data)
        # set common URL fields where appropriate
        if isinstance(data,dict):
            if data.get('@type')=='BlogPosting':
                data['url']=page_url; data['mainEntityOfPage']=page_url
            elif data.get('@type')=='Blog': data['url']=page_url
            elif '@graph' in data:
                for item in data['@graph']:
                    t=item.get('@type')
                    types=t if isinstance(t,list) else [t]
                    if 'WebSite' in types: item['url']=base+'/'
                    if 'WebPage' in types: item['url']=page_url
                    if 'LiquorStore' in types or 'Store' in types: item['url']=base+'/'
        return '<script type="application/ld+json">'+json.dumps(data,separators=(',',':'))+'</script>'
    return re.sub(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>',repl,text,flags=re.S|re.I)

def main():
    cfg=json.loads(CONFIG.read_text()) if CONFIG.exists() else {}
    base=clean_url(cfg.get('site_url'))
    if not base:
        print('SEO domain setup skipped: set data/site_config.json -> site_url after you buy/connect the domain.')
        return
    urls=[]
    for path in html_files():
        page_url=public_url(path,base); urls.append((page_url,path))
        text=path.read_text(encoding='utf-8')
        text=set_link_tag(text,'canonical',page_url)
        text=set_meta_property(text,'og:url',page_url)
        text=absolutize_jsonld(text,page_url,base)
        path.write_text(text,encoding='utf-8')
    sm=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u,p in urls:
        sm.append('  <url>')
        sm.append(f'    <loc>{html.escape(u)}</loc>')
        sm.append('    <changefreq>'+('daily' if '/blog/' in u else 'weekly')+'</changefreq>')
        sm.append('  </url>')
    sm.append('</urlset>')
    (ROOT/'sitemap.xml').write_text('\n'.join(sm)+'\n',encoding='utf-8')
    (ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n',encoding='utf-8')
    print(f'SEO domain configured: {base}; sitemap has {len(urls)} URLs.')
if __name__=='__main__': main()
