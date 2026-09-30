const fallback=[
{slug:'classic-old-fashioned',title:'How to Make a Classic Old Fashioned',category:'Cocktail Recipe',date:'2026-09-30',excerpt:'A balanced, approachable recipe with whiskey, bitters, a touch of sweetness, and citrus.',minutes:4},
{slug:'wine-pairing-basics',title:'Wine Pairing Basics Without the Stress',category:'Wine Guide',date:'2026-09-29',excerpt:'Simple pairing ideas you can actually use for dinner, parties, and gifts.',minutes:5},
{slug:'margarita-at-home',title:'A Fresh Margarita You Can Make at Home',category:'Cocktail Recipe',date:'2026-09-28',excerpt:'A bright, citrus-forward classic with an easy ratio to remember.',minutes:4},
{slug:'home-bar-starter-guide',title:'A Simple Starter Guide to Building a Home Bar',category:'Spirits Guide',date:'2026-09-27',excerpt:'A practical way to build a flexible home bar without buying everything at once.',minutes:6},
{slug:'easy-party-punch',title:'Easy Party Punch for a Small Gathering',category:'Entertaining',date:'2026-09-26',excerpt:'A simple citrus-forward batch drink you can scale for your next gathering.',minutes:4},
{slug:'whiskey-basics',title:'Whiskey Basics: Bourbon, Rye and More',category:'Spirits Guide',date:'2026-09-25',excerpt:'A beginner-friendly look at common whiskey styles and how they differ.',minutes:6}
];
const grid=document.getElementById('postList');const search=document.getElementById('searchPosts');const no=document.getElementById('noResults');let posts=[];
function render(list){grid.innerHTML=list.map(p=>`<a class="blog-tile" href="posts/${p.slug}.html"><div class="meta"><span class="tag">${p.category}</span><span>${new Date(p.date+'T12:00:00').toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'})}</span></div><h3>${p.title}</h3><p>${p.excerpt}</p><span class="read">${p.minutes||5} min read →</span></a>`).join('');no.hidden=list.length>0}
fetch('../data/posts.json').then(r=>r.ok?r.json():Promise.reject()).then(data=>{posts=data;render(posts)}).catch(()=>{posts=fallback;render(posts)});
search?.addEventListener('input',()=>{const q=search.value.toLowerCase().trim();render(posts.filter(p=>`${p.title} ${p.category} ${p.excerpt}`.toLowerCase().includes(q)))});
document.getElementById('year').textContent=new Date().getFullYear();
