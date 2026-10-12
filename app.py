from fastapi import FastAPI,Request,Form
from fastapi.responses import HTMLResponse,JSONResponse,RedirectResponse
import os,psutil,subprocess,hashlib,shutil,zipfile,pathlib,time,glob,threading
app=FastAPI(docs_url=None,redoc_url=None)
B='/root/apps';os.makedirs(B,exist_ok=True);S='cloudpusat54';P=hashlib.sha256(('cloud54'+S).encode()).hexdigest()
def ok(r):return r.cookies.get('auth','')==P
def is_run(bp,bn):
 pf=os.path.join(bp,'.pid')
 if os.path.exists(pf):
  try:
   pid=int(open(pf).read().strip() or "0")
   if pid and psutil.pid_exists(pid):return True,pid
  except:pass
 for pr in psutil.process_iter(['pid','cmdline']):
  try:
   if pr.cwd()==bp:return True,pr.info['pid']
   c=' '.join(pr.info['cmdline'] or [])
   if bp in c and 'python' in c:return True,pr.info['pid']
  except:continue
 return False,0
def auto_fix_bot(bp):
 try:
  for pat in ['*.db-shm','*.db-wal','*.sqlite-shm','*.sqlite-wal','*.session-journal','.pid','bot.log']:
   for ff in glob.glob(os.path.join(bp,pat)):
    try:os.remove(ff)
    except:pass
  for sd in [os.path.join(bp,'FILE_PO/session/bot'), os.path.join(bp,'session/bot'), os.path.join(bp,'session'), os.path.join(bp,'FILE_PO/session')]:
   if os.path.exists(sd):
    for ff in glob.glob(os.path.join(sd,'*.session-journal')):
     try:os.remove(ff)
     except:pass
   os.makedirs(sd,exist_ok=True)
  os.makedirs(os.path.join(bp,'FILE_PO/session/bot'),exist_ok=True)
  return True
 except:return False
def start_bot_process(bp):
 cf=os.path.join(bp,'.command');cmd=pathlib.Path(cf).read_text().strip() if os.path.exists(cf) else 'python3 main.py'
 venv="/root/panel-venv/bin/python";py=venv if os.path.exists(venv) else "python3"
 if "python3" in cmd:cmd=cmd.replace("python3",py)
 if "-u" not in cmd and py in cmd:cmd=cmd.replace(py,f"{py} -u")
 full=f"cd {bp} && nohup {cmd} > bot.log 2>&1 & echo $!"
 r=subprocess.run(full,shell=True,capture_output=True,text=True,timeout=10)
 pid_str=r.stdout.strip()
 try:
  if pid_str:open(os.path.join(bp,'.pid'),'w').write(pid_str)
 except:pass
 return pid_str
def heal_loop():
 while True:
  time.sleep(30)
  try:
   for n in os.listdir(B):
    bp=os.path.join(B,n)
    if not os.path.isdir(bp):continue
    if os.path.exists(os.path.join(bp,'.autorun')):
     run,_=is_run(bp,n)
     if not run:
      auto_fix_bot(bp);time.sleep(1);start_bot_process(bp)
  except:pass
threading.Thread(target=heal_loop,daemon=True).start()

LOGIN='<html><head><meta name=viewport content="width=device-width,initial-scale=1"><title>CloudPusat54 Premium</title><style>body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;background:#08070e;color:#fff;font-family:Inter,system-ui}body::before{content:"";position:fixed;inset:0;background:radial-gradient(900px at 50% 0%,rgba(250,204,21,.28),transparent 70%),radial-gradient(700px at 0% 100%,rgba(120,60,255,.35),transparent 60%);pointer-events:none}.bx{width:92%;max-width:380px;background:rgba(15,15,28,.92);border:1px solid rgba(255,255,255,.1);border-radius:28px;padding:30px;text-align:center;position:relative;z-index:1;box-shadow:0 20px 60px rgba(0,0,0,.6)}.lg{font-weight:900;font-size:28px;letter-spacing:-.5px}.lg span{color:#facc15}.sub{font-size:11px;color:#64748b;margin-top:4px;letter-spacing:2px}.marquee{overflow:hidden;white-space:nowrap;background:linear-gradient(90deg,rgba(250,204,21,.12),rgba(250,204,21,.04));border:1px solid rgba(250,204,21,.18);border-radius:14px;padding:10px 0;margin-bottom:20px;box-shadow:0 0 20px rgba(250,204,21,.15) inset}.marquee span{display:inline-block;padding-left:100%;animation:marq 14s linear infinite;color:#facc15;font-weight:900;font-size:13px;letter-spacing:2px;text-shadow:0 0 10px rgba(250,204,21,.8)}.copy{margin-top:18px;font-size:10px;color:#475569;letter-spacing:1px;line-height:1.5}.copy b{color:#64748b}@keyframes marq{0%{transform:translate(0,0)}100%{transform:translate(-100%,0)}}input{width:100%;margin-top:12px;padding:14px 16px;border-radius:14px;border:1px solid rgba(255,255,255,.1);background:rgba(0,0,0,.35);color:#fff;outline:none;font-size:14px}input:focus{border-color:rgba(250,204,21,.4);box-shadow:0 0 0 3px rgba(250,204,21,.1)}button{width:100%;margin-top:18px;padding:14px;border-radius:14px;border:0;background:linear-gradient(90deg,#facc15,#fde047);color:#000;font-weight:900;font-size:14px;cursor:pointer;box-shadow:0 8px 20px rgba(250,204,21,.25)}</style></head><body><div class=bx><div class=marquee><span>⚡ WELCOME TO Pyrunnercloud54 ⚡ WELCOME TO Pyrunnercloud54 ⚡ WELCOME TO Pyrunnercloud54 ⚡</span></div><div class=lg>Cloud<span>Pusat54</span></div><div class=sub>PREMIUM PANEL V12</div><form method=post action=/login><input name=user placeholder=Username: admin><input name=pass type=password placeholder=Password: cloud54><button>LOGIN PREMIUM</button></form><div class=copy><b>© 2026 CLOUDPUSAT54</b><br>All Rights Reserved - Premium Auto-Fix System<br>Secure & Private</div></div></body></html>'

MAIN='''<html><head><meta name=viewport content="width=device-width,initial-scale=1"><title>CloudPusat54 Premium</title><style>
*{box-sizing:border-box;font-family:Inter,system-ui}body{margin:0;background:#08070e;color:#cbd5e1;padding-bottom:110px}
body::before{content:'';position:fixed;inset:0;background:radial-gradient(900px at 50% 0%,rgba(250,204,21,.22),transparent 70%),radial-gradient(700px at 0% 100%,rgba(80,30,180,.4),transparent 60%);pointer-events:none}
.wrap{position:relative;z-index:1;max-width:480px;margin:0 auto;padding:14px}
.h{position:sticky;top:0;z-index:20;display:flex;justify-content:space-between;align-items:center;padding:14px 18px;background:rgba(8,10,18,.9);backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,255,255,.08);margin:-14px -14px 14px -14px}
.logo{font-weight:900;font-size:19px;color:#fff}.logo span{color:#facc15}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:rgba(255,255,255,.08);border-radius:22px;overflow:hidden;margin-bottom:18px}
.stat{background:rgba(15,15,28,.9);padding:16px}.stat b{font-size:22px;color:#fff;display:block;margin-top:4px;font-weight:800}
.bar{height:3px;background:rgba(0,0,0,.4);border-radius:10px;margin-top:10px;overflow:hidden}.bar i{display:block;height:100%;border-radius:10px}
.sec{background:rgba(15,15,28,.75);border:1px solid rgba(255,255,255,.08);border-radius:26px;padding:18px;backdrop-filter:blur(20px)}
.bot{display:flex;justify-content:space-between;align-items:center;padding:14px;background:rgba(10,10,18,.6);border:1px solid rgba(255,255,255,.06);border-radius:18px;margin-top:10px}
.bot.on{border-color:rgba(250,204,21,.25);background:linear-gradient(90deg,rgba(250,204,21,.08),rgba(10,10,18,.6))}
.dot{width:9px;height:9px;border-radius:50%}.dot.on{background:#22c55e;box-shadow:0 0 10px #22c55e}.dot.off{background:#334155}
.badge{font-size:9px;padding:3px 8px;border-radius:20px;font-weight:800;border:1px solid}.badge.on{color:#4ade80;background:rgba(74,222,128,.1)}.badge.off{color:#64748b;background:rgba(100,116,139,.1)}
.btn{padding:7px 12px;border-radius:10px;border:1px solid rgba(255,255,255,.08);font-size:11px;font-weight:700;cursor:pointer}.btn-run{background:#facc15;color:#000;font-weight:900}.btn-stop{background:rgba(0,0,0,.3);color:#ef4444}.btn-log{background:rgba(0,0,0,.3);color:#94a3b8}
.inp{width:100%;padding:12px 14px;background:rgba(0,0,0,.3);border:1px solid rgba(255,255,255,.08);border-radius:12px;color:#fff;outline:none;margin-bottom:10px}
.logbox{background:rgba(0,0,0,.4);border:1px solid rgba(255,255,255,.06);border-radius:12px;padding:12px;font-family:monospace;font-size:11px;max-height:300px;overflow:auto;color:#facc15;white-space:pre-wrap;margin-top:12px}
.bottom{position:fixed;bottom:14px;left:50%;transform:translateX(-50%);width:92%;max-width:400px;background:rgba(15,15,28,.95);border:1px solid rgba(255,255,255,.12);border-radius:26px;display:flex;padding:6px;z-index:9999}
.bottom div{flex:1;text-align:center;padding:14px 6px;border-radius:18px;font-size:12px;font-weight:800;color:#6b7280;cursor:pointer}.bottom div.on{background:rgba(250,204,21,.15);color:#facc15}
</style></head><body>
<div class=wrap>
<div class=h><div class=logo>Cloud<span>Pusat54</span> <span style="font-size:10px;background:rgba(250,204,21,.2);color:#facc15;padding:3px 8px;border-radius:20px">PREMIUM V12 AUTO-FIX</span></div><div style="display:flex;gap:10px;align-items:center"><span style="font-size:11px;color:#4b5563" id="clk"></span><a href="/logout" style="color:#94a3b8;text-decoration:none;font-size:12px;border:1px solid rgba(255,255,255,.1);padding:5px 10px;border-radius:20px">Logout</a></div></div>
<div class=grid><div class=stat><label>CPU</label><b id="cpu">-</b><div class=bar><i id="cb" style="width:10%;background:linear-gradient(90deg,#facc15,#fef08a)"></i></div></div><div class=stat><label>RAM</label><b id="ram">-</b><div class=bar><i id="rb" style="width:30%;background:linear-gradient(90deg,#8b5cf6,#a78bfa)"></i></div></div><div class=stat><label>DISK</label><b id="disk">-</b><div class=bar><i id="db" style="width:50%;background:linear-gradient(90deg,#06b6d4,#67e8f9)"></i></div></div></div>
<div id="p1"><div class=sec><div style="display:flex;justify-content:space-between;margin-bottom:12px"><b style="color:#fff;font-size:13px">MY BOTS (AUTO-FIX ACTIVE)</b><span id="cnt" style="font-size:11px;color:#475569"></span></div><div id="bots">Loading...</div><div id="rlog" class=logbox style="display:none"></div></div></div>
<div id="p2" style="display:none"><div class=sec><div style="display:flex;justify-content:space-between"><span id="cur" style="color:#facc15;font-family:monospace;font-size:11px">/root/apps</span><button class=btn onclick="lf('/root/apps')">Root</button></div><div id="fl" style="margin-top:10px"></div></div></div>
<div id="p3" style="display:none"><div class=sec><b style="color:#fff">Deploy Premium Bot</b><p style="color:#64748b;font-size:12px">ZIP + Auto-Fix</p><input id="n" class=inp placeholder="Nama bot"><input id="cmd" class=inp value="python3 main.py"><input type="file" id="z" style="margin:8px 0;color:#64748b"><button class="btn btn-run" style="width:100%;padding:13px" onclick="dp()">Deploy Premium</button><div id="dl" class=logbox style="display:none"></div></div></div>
</div>
<div class=bottom><div id="b1" class="on" onclick="sh(1)">Monitor</div><div id="b2" onclick="sh(2)">Files</div><div id="b3" onclick="sh(3)">Deploy</div></div>
<script>
let cur='/root/apps',sel=null;
function sh(x){
 document.getElementById('p1').style.display=x==1?'block':'none';
 document.getElementById('p2').style.display=x==2?'block':'none';
 document.getElementById('p3').style.display=x==3?'block':'none';
 document.getElementById('b1').className=x==1?'on':'';
 document.getElementById('b2').className=x==2?'on':'';
 document.getElementById('b3').className=x==3?'on':'';
 if(x==2)lf(cur);if(x==1)lm();
}
function lm(){
 fetch('/api/s').then(r=>r.json()).then(d=>{
  document.getElementById('cpu').innerText=d.c+'%';document.getElementById('ram').innerText=d.m+'GB';document.getElementById('disk').innerText=d.d+'GB';document.getElementById('cb').style.width=d.c+'%';
 });
 fetch('/api/b').then(r=>r.json()).then(d=>{
  let h='';document.getElementById('cnt').innerText=d.length+' bots';
  for(let x of d){
   let on=x[1]=='running';
   h+='<div class="bot '+(on?'on':'')+'"><div style="display:flex;align-items:center;gap:11px"><div class="dot '+(on?'on':'off')+'"></div><div><div style="font-weight:700;color:#fff;font-size:14px">'+x[0]+(x[3]?' <span style="font-size:9px;background:#facc15;color:#000;padding:2px 6px;border-radius:10px">AUTO</span>':'')+'</div><div style="display:flex;gap:6px;margin-top:4px"><span class="badge '+(on?'on':'off')+'">'+(on?'LIVE':'OFF')+'</span><span style="font-size:11px;color:#475569">#'+(x[2]||'0')+'</span></div></div></div><div style="display:flex;gap:5px"><button class="btn btn-run" onclick="rb(\\''+x[0]+'\\')">Run</button><button class="btn btn-stop" onclick="sb(\\''+x[0]+'\\')">Stop</button><button class="btn btn-log" onclick="lb(\\''+x[0]+'\\')">Log</button></div></div>';
  }
  document.getElementById('bots').innerHTML=h||'<div style="text-align:center;padding:20px;color:#334155">No bots</div>';
 });
}
function rb(n){document.getElementById('rlog').style.display='block';document.getElementById('rlog').innerText='Auto-fix & Starting '+n+'...';fetch('/api/bot/'+n+'/start',{method:'POST'}).then(r=>r.json()).then(d=>{document.getElementById('rlog').innerText=d.log;lm()})}
function sb(n){fetch('/api/bot/'+n+'/stop',{method:'POST'}).then(()=>{document.getElementById('rlog').style.display='block';document.getElementById('rlog').innerText='Stopped '+n;lm()})}
function lb(n){fetch('/api/bot/'+n+'/log').then(r=>r.text()).then(t=>{document.getElementById('rlog').style.display='block';document.getElementById('rlog').innerText=t.slice(-4000)||'No log'})}
function lf(p){cur=p;document.getElementById('cur').innerText=p;fetch('/api/ls?path='+encodeURIComponent(p)).then(r=>r.json()).then(d=>{let h='';for(let x of d){let sp=x.p.replace(/'/g,"_");h+='<div class=file onclick="sl(\\''+sp+'\\','+x.d+')"><span><b>'+(x.d?'[DIR]':'[FILE]')+' '+x.n+'</b></span></div>'}document.getElementById('fl').innerHTML=h})}
function sl(p,d){sel=p;if(d)lf(p)}
function dp(){let n=document.getElementById('n').value;if(!n)return alert('Isi nama');let fd=new FormData();fd.append('name',n);fd.append('command',document.getElementById('cmd').value);fd.append('file',document.getElementById('z').files[0]);document.getElementById('dl').style.display='block';document.getElementById('dl').innerText='Uploading...';fetch('/api/dp',{method:'POST',body:fd}).then(r=>r.json()).then(d=>{document.getElementById('dl').innerText=d.log;lm();sh(1)})}
setInterval(function(){document.getElementById('clk').innerText=new Date().toLocaleTimeString('id-ID',{hour:'2-digit',minute:'2-digit'})},1000);
lm();setInterval(lm,3000);
</script></body></html>'''

@app.get('/login',response_class=HTMLResponse)
async def a():return HTMLResponse(LOGIN)
@app.post('/login')
async def b(user: str=Form(...),pass_: str=Form(...,alias='pass')):
 if user=='admin' and hashlib.sha256((pass_+S).encode()).hexdigest()==P:
  r=RedirectResponse('/',302);r.set_cookie('auth',P,max_age=86400*30,httponly=True);return r
 return HTMLResponse(LOGIN,401)
@app.get('/logout')
async def c():
 r=RedirectResponse('/login',302);r.delete_cookie('auth');return r
@app.get('/',response_class=HTMLResponse)
async def d(request: Request):
 if not ok(request):return RedirectResponse('/login',302)
 return HTMLResponse(MAIN)
@app.get('/api/b')
async def e():
 o=[]
 for n in os.listdir(B):
  p=os.path.join(B,n)
  if os.path.isdir(p) and not n.startswith('.'):
   run,pid=is_run(p,n)
   auto=os.path.exists(os.path.join(p,'.autorun'))
   o.append([n,'running' if run else 'stopped',pid,auto])
 return JSONResponse(sorted(o))
@app.post('/api/bot/{name}/start')
async def f(name: str):
 bp=os.path.join(B,name)
 auto_fix_bot(bp)
 for pr in psutil.process_iter(['pid']):
  try:
   if pr.cwd()==bp:pr.kill()
  except:pass
 time.sleep(0.5)
 pid=start_bot_process(bp)
 time.sleep(1.5)
 run,pid2=is_run(bp,name)
 log=""
 try:log=open(os.path.join(bp,'bot.log'),errors='ignore').read()[-2500:]
 except:pass
 if run:
  open(os.path.join(bp,'.autorun'),'w').write('1')
  return JSONResponse({'log':f'✅ PREMIUM AUTO-FIX LIVE {name} PID {pid2}\n{log}'})
 else:
  return JSONResponse({'log':f'⚠️ AUTO-FIX TRY {name} - Will auto retry in 30s\n{log}'})
@app.post('/api/bot/{name}/stop')
async def g(name: str):
 bp=os.path.join(B,name)
 for pr in psutil.process_iter(['pid']):
  try:
   if pr.cwd()==bp:pr.kill()
  except:pass
 try:os.remove(os.path.join(bp,'.pid'));os.remove(os.path.join(bp,'.autorun'))
 except:pass
 return JSONResponse({'ok':True})
@app.get('/api/bot/{name}/log')
async def g2(name: str):
 p=os.path.join(B,name,'bot.log')
 return HTMLResponse(open(p,errors='ignore').read()[-5000:] if os.path.exists(p) else "no log")
@app.get('/api/ls')
async def h(path: str):
 if not path.startswith('/root/'):path=B
 o=[]
 for nm in sorted(os.listdir(path)):
  if nm.startswith('.'):continue
  fp=os.path.join(path,nm);o.append({'n':nm,'p':fp,'d':os.path.isdir(fp)})
 return JSONResponse(o)
@app.post('/api/dp')
async def n(request: Request):
 f=await request.form();na=f.get('name');fi=f.get('file');de=os.path.join(B,na);os.makedirs(de,exist_ok=True)
 log=f"Deploy {na}\n"
 if fi:
  da=await fi.read();zp=os.path.join(de,'a.zip');open(zp,'wb').write(da)
  try:
   with zipfile.ZipFile(zp,'r') as z:z.extractall(de)
   log+=f"Extract OK - Premium Auto-fix ON\n"
  except Exception as e:log+=f"Fail {e}\n"
  try:os.remove(zp)
  except:pass
 open(os.path.join(de,'.command'),'w').write(f.get('command') or 'python3 main.py')
 auto_fix_bot(de)
 return JSONResponse({'ok':True,'log':log})
@app.get('/api/s')
async def o():
 return JSONResponse({'c':round(psutil.cpu_percent(),1),'m':round(psutil.virtual_memory().used/1024/1024/1024,1),'d':round(psutil.disk_usage('/').used/1024/1024/1024,1)})