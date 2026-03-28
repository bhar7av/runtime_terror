  /* ── THEME ── apply before paint to avoid flash */
  (function() {
    if (localStorage.getItem('swastya-theme') === 'light') {
      document.documentElement.classList.add('light');
    }
  })();

  function toggleTheme() {
    const isLight = document.documentElement.classList.toggle('light');
    const btn = document.getElementById('themeToggle');
    btn.textContent = isLight ? '☀️' : '🌙';
    btn.title = isLight ? 'Switch to dark mode' : 'Switch to light mode';
    localStorage.setItem('swastya-theme', isLight ? 'light' : 'dark');
  }

  /* sync button icon after DOM loads */
  window.addEventListener('DOMContentLoaded', function() {
    const isLight = document.documentElement.classList.contains('light');
    const btn = document.getElementById('themeToggle');
    if (isLight) { btn.textContent = '☀️'; btn.title = 'Switch to dark mode'; }
  });

  /* ── CHAT ── */
  function handleChatKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  }

  function sendMessage() {
    const input = document.getElementById('chatInput');
    const msg = input.value.trim();
    if (!msg) return;
    const messages = document.getElementById('chatMessages');

    const userDiv = document.createElement('div');
    userDiv.className = 'msg user';
    userDiv.innerHTML = `<div class="msg-avatar">U</div><div class="msg-bubble">${msg}</div>`;
    messages.appendChild(userDiv);
    input.value = '';
    messages.scrollTop = messages.scrollHeight;

    setTimeout(() => {
      const aiDiv = document.createElement('div');
      aiDiv.className = 'msg ai';
      aiDiv.innerHTML = `<div class="msg-avatar">🤖</div><div><div class="msg-bubble" style="color:var(--text3);font-style:italic">Analyzing with multi-agent system…</div></div>`;
      messages.appendChild(aiDiv);
      messages.scrollTop = messages.scrollHeight;
      setTimeout(() => {
        const bubble = aiDiv.querySelector('.msg-bubble');
        bubble.style.fontStyle = 'normal';
        bubble.style.color = 'var(--text)';
        bubble.innerHTML = `Received your message. AI agents are processing your symptoms for severity assessment, first aid guidance, and doctor recommendations. <span style="color:var(--text3);font-size:12px">(Connect to Tarkshya's backend for live responses)</span>`;
        messages.scrollTop = messages.scrollHeight;
      }, 1200);
    }, 400);
  }

  /* ── FILE UPLOAD ── */
  function handleFileUpload(e) {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = ev => {
      document.getElementById('uploadedImg').src = ev.target.result;
      document.getElementById('uploadPreview').style.display = 'block';
    };
    reader.readAsDataURL(file);
  }

  /* ── SMOOTH SCROLL ── */
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      e.preventDefault();
      const el = document.querySelector(a.getAttribute('href'));
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    });
  });

/* ===============================
   UI ENHANCEMENTS
================================ */

/* Auto expand textarea */
const input = document.getElementById("chatInput");

input.addEventListener("input",()=>{
  input.style.height="auto";
  input.style.height=input.scrollHeight+"px";
});

/* Enter to send */
function handleChatKey(e){
  if(e.key==="Enter" && !e.shiftKey){
    e.preventDefault();
    sendMessage();
  }
}

/* Fake send animation */
function sendMessage(){
  if(!input.value.trim()) return;

  const box=document.getElementById("chatMessages");

  const msg=document.createElement("div");
  msg.className="msg user";
  msg.innerHTML=`
    <div class="msg-avatar">U</div>
    <div class="msg-bubble">${input.value}</div>
  `;

  box.appendChild(msg);
  input.value="";
  input.style.height="42px";

  box.scrollTop=box.scrollHeight;
}

/* Theme toggle */
function toggleTheme(){
  document.documentElement.classList.toggle("light");

  const btn=document.getElementById("themeToggle");

  if(document.documentElement.classList.contains("light")){
    btn.textContent="☀️";
    btn.title="Switch to dark mode";
  }else{
    btn.textContent="🌙";
    btn.title="Switch to light mode";
  }
}

/* Smooth reveal on scroll */
const observer=new IntersectionObserver(entries=>{
  entries.forEach(e=>{
    if(e.isIntersecting){
      e.target.style.opacity=1;
      e.target.style.transform="translateY(0)";
    }
  });
},{threshold:.1});

document.querySelectorAll("section").forEach(sec=>{
  sec.style.opacity=0;
  sec.style.transform="translateY(40px)";
  observer.observe(sec);
});