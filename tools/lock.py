"""Encrypt the yearbook page behind a passcode (AES-256-GCM, PBKDF2-SHA256). Usage: python3 lock.py <passcode> <in.html> <out.html>"""
import sys, os, base64, json
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
passcode, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
salt, iv = os.urandom(16), os.urandom(12)
key = PBKDF2HMAC(hashes.SHA256(), 32, salt, 200000).derive(passcode.strip().lower().encode())
ct = AESGCM(key).encrypt(iv, open(src, "rb").read(), None)
b64 = lambda b: base64.b64encode(b).decode()
gate = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Constellation · UW–Madison MSTP 2026</title>
<meta name="description" content="The 2026 UW–Madison MSTP retreat yearbook.">
<meta name="theme-color" content="#070B1C">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%E2%9C%A8%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,500&family=Nunito:wght@400;600;700&display=swap">
<style>
  html,body{height:100%;margin:0} body{background:radial-gradient(120% 90% at 50% 110%,#1A1F4A 0%,#0E1636 45%,#070B1C 100%);color:#EEF1FF;font-family:"Nunito",sans-serif;display:grid;place-items:center;overflow:hidden}
  canvas{position:fixed;inset:0;width:100%;height:100%}
  .g{position:relative;text-align:center;padding:24px;max-width:420px}
  .eyebrow{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:#7F8AB8;font-weight:700}
  h1{font-family:"Cormorant Garamond",Georgia,serif;font-weight:500;font-size:44px;margin:6px 0 4px;line-height:1}
  h1 em{font-style:italic;color:#F5DFA3}
  p{color:#B9C2E6;font-size:14px;margin:0 0 22px}
  form{display:flex;gap:8px;justify-content:center}
  input{flex:1;max-width:240px;border:1px solid rgba(185,194,230,.25);background:rgba(14,20,52,.7);color:#EEF1FF;font:inherit;font-size:15px;padding:11px 14px;border-radius:999px;outline:none;text-align:center;letter-spacing:.08em}
  input:focus{border-color:#F5DFA3}
  button{border:0;background:#F5DFA3;color:#1A1400;font:inherit;font-weight:800;font-size:14px;padding:11px 18px;border-radius:999px;cursor:pointer}
  button:disabled{opacity:.6;cursor:wait}
  .msg{min-height:20px;font-size:13px;color:#F9A995;margin-top:12px}
  .hint{font-size:12px;color:#7F8AB8;margin-top:26px}
</style></head>
<body><canvas id="s"></canvas>
<div class="g"><div class="eyebrow">UW–Madison MSTP · Retreat 2026</div><h1>The <em>Constellation</em></h1>
<p>This sky is for the program. Enter the passcode from the email to open it.</p>
<form id="f"><input id="p" type="password" autocomplete="current-password" placeholder="passcode" autofocus><button id="b" type="submit">Open</button></form>
<div class="msg" id="m"></div>
<div class="hint">Can't find it? Ask anyone in the program, or email Sophia.</div></div>
<script>
(async () => {
  const c = document.getElementById("s"), x = c.getContext("2d"); let W, H; const st = Array.from({length: 160}, () => ({x: Math.random(), y: Math.random(), r: Math.random()*1.2+.3, p: Math.random()*6.28}));
  const rs = () => { W = c.width = innerWidth; H = c.height = innerHeight; }; rs(); addEventListener("resize", rs); let t = 0;
  (function d(){ t += .016; x.clearRect(0,0,W,H); st.forEach(s => { x.globalAlpha = .3 + .4*(.5+.5*Math.sin(t+s.p)); x.fillStyle = "#DDE4FF"; x.beginPath(); x.arc(s.x*W, s.y*H, s.r, 0, 6.28); x.fill(); }); requestAnimationFrame(d); })();
  const SALT = "%SALT%", IV = "%IV%", CT = "%CT%";
  const b = s => Uint8Array.from(atob(s), ch => ch.charCodeAt(0));
  async function open(pass) {
    const km = await crypto.subtle.importKey("raw", new TextEncoder().encode(pass.trim().toLowerCase()), "PBKDF2", false, ["deriveKey"]);
    const key = await crypto.subtle.deriveKey({name: "PBKDF2", salt: b(SALT), iterations: 200000, hash: "SHA-256"}, km, {name: "AES-GCM", length: 256}, false, ["decrypt"]);
    const plain = await crypto.subtle.decrypt({name: "AES-GCM", iv: b(IV)}, key, b(CT));
    const html = new TextDecoder().decode(plain);
    try { sessionStorage.setItem("mstp-pass", pass); } catch (e) {}
    document.open(); document.write(html); document.close();
  }
  const f = document.getElementById("f"), p = document.getElementById("p"), m = document.getElementById("m"), bt = document.getElementById("b");
  f.addEventListener("submit", async e => { e.preventDefault(); bt.disabled = true; m.textContent = "Opening the sky…"; try { await open(p.value); } catch (err) { m.textContent = "That's not it — check the email and try again."; bt.disabled = false; p.select(); } });
  try { const saved = sessionStorage.getItem("mstp-pass"); if (saved) { m.textContent = "Opening the sky…"; await open(saved); } } catch (e) { m.textContent = ""; }
})();
</script></body></html>'''
open(dst, "w").write(gate.replace("%SALT%", b64(salt)).replace("%IV%", b64(iv)).replace("%CT%", b64(ct)))
print("locked:", os.path.getsize(dst)//1024, "KB")
