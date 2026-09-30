const ageGate=document.getElementById('ageGate');
const enterSite=document.getElementById('enterSite');
const leaveSite=document.getElementById('leaveSite');
const menuToggle=document.getElementById('menuToggle');
const nav=document.getElementById('nav');
document.body.classList.add('locked');
if(localStorage.getItem('paolaMarketAgeVerified')==='yes'){ageGate.classList.add('hidden');document.body.classList.remove('locked')}
enterSite?.addEventListener('click',()=>{localStorage.setItem('paolaMarketAgeVerified','yes');ageGate.classList.add('hidden');document.body.classList.remove('locked')});
leaveSite?.addEventListener('click',()=>{window.location.href='https://www.google.com/'});
menuToggle?.addEventListener('click',()=>{const open=nav.classList.toggle('open');menuToggle.setAttribute('aria-expanded',open?'true':'false')});
nav?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('open');menuToggle.setAttribute('aria-expanded','false')}));
const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){setTimeout(()=>entry.target.classList.add('visible'),Number(entry.target.dataset.delay||0));observer.unobserve(entry.target)}}),{threshold:.12});
document.querySelectorAll('.reveal').forEach(el=>observer.observe(el));
document.getElementById('year').textContent=new Date().getFullYear();
window.addEventListener('mousemove',e=>{if(window.innerWidth<1100)return;const logo=document.querySelector('.hero-logo');if(!logo)return;const x=(e.clientX/window.innerWidth-.5)*8;const y=(e.clientY/window.innerHeight-.5)*8;logo.style.transform=`translate(${x}px,${y}px)`});
