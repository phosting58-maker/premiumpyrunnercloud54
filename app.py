from fastapi import FastAPI,Request,Form
from fastapi.responses import HTMLResponse,JSONResponse,RedirectResponse
import os,psutil,subprocess,hashlib,zipfile,pathlib,time,glob,threading,datetime
app=FastAPI(docs_url=None,redoc_url=None)
B='/root/apps';os.makedirs(B,exist_ok=True);S='cloudpusat54';P=hashlib.sha256(('cloud54'+S).encode()).hexdigest()
LICENSE_DAYS = 30
INSTALL_FILE='/root/panel/.install_date'
BACKUP1='/root/.license_backup'
BACKUP2='/root/apps/.license_backup'
LICENSE_OWNER='CLOUDPUSAT54 PREMIUM'
WA_NUMBER='6285218016760'

def get_install_date():
 try:
  # ANTI RESET IP - CEK 3 TEMPAT
  for p in [INSTALL_FILE,BACKUP1,BACKUP2]:
   if os.path.exists(p):
    d=open(p).read().strip()
    if d:
     # Restore ke semua tempat biar aman
     try:
      os.makedirs('/root/panel',exist_ok=True)
      open(INSTALL_FILE,'w').write(d)
      open(BACKUP1,'w').write(d)
      open(BACKUP2,'w').write(d)
     except: pass
     return datetime.datetime.strptime(d,'%Y-%m-%d')
  # Kalo ga ada sama sekali, baru bikin baru
  now=datetime.datetime.now().strftime('%Y-%m-%d')
  os.makedirs('/root/panel',exist_ok=True)
  open(INSTALL_FILE,'w').write(now)
  open(BACKUP1,'w').write(now)
  open(BACKUP2,'w').write(now)
  return datetime.datetime.strptime(now,'%Y-%m-%d')
 except:return datetime.datetime.now()

def get_expiry():return get_install_date() + datetime.timedelta(days=LICENSE_DAYS)
def days_left():
 try:return (get_expiry() - datetime.datetime.now()).days
 except:return LICENSE_DAYS
def is_expired():return days_left() < 0
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
  for sd in [os.path.join(bp,'FILE_PO/session/bot'), os.path.join(bp,'session/bot')]:
   os.makedirs(sd,exist_ok=True)
   for ff in glob.glob(os.path.join(sd,'*.session-journal')):
    try:os.remove(ff)
    except:pass
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
   if is_expired():continue
   for n in os.listdir(B):
    bp=os.path.join(B,n)
    if not os.path.isdir(bp):continue
    if os.path.exists(os.path.join(bp,'.autorun')):
     run,_=is_run(bp,n)
     if not run:auto_fix_bot(bp);time.sleep(1);start_bot_process(bp)
  except:pass
threading.Thread(target=heal_loop,daemon=True).start()

def render_login():
 exp=get_expiry().strftime('%d %B %Y');dl=days_left();own=LICENSE_OWNER;wa=WA_NUMBER
 lic_color="#4ade80" if dl>10 else "#facc15" if dl>3 else "#ef4444"
 lic_text=f"LICENSE ACTIVE - {dl} HARI LAGI" if dl>=0 else "LICENSE EXPIRED!"
 return f'<html><head><meta name=viewport content="width=device-width,initial-scale=1"><title>CloudPusat54 Premium</title><style>body{{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;background:#08070e;color:#fff;font-family:Inter,system-ui}}body::before{{content:"";position:fixed;inset:0;background:radial-gradient(900px at 50% 0%,rgba(250,204,21,.28),transparent 70%),radial-gradient(700px at 0% 100%,rgba(120,60,255,.35),transparent 60%);pointer-events:none}}.bx{{width:92%;max-width:380px;background:rgba(15,15,28,.92);border:1px solid rgba(255,255,255,.1);border-radius:28px;padding:30px;text-align:center;position:relative;z-index:1;box-shadow:0 20px 60px rgba(0,0,0,.6)}}.lg{{font-weight:900;font-size:28px}}.lg span{{color:#facc15}}.sub{{font-size:11px;color:#64748b;margin-top:4px;letter-spacing:2px}}.marquee{{overflow:hidden;white-space:nowrap;background:linear-gradient(90deg,rgba(250,204,21,.12),rgba(250,204,21,.04));border:1px solid rgba(250,204,21,.18);border-radius:14px;padding:10px 0;margin-bottom:14px}}.marquee span{{display:inline-block;padding-left:100%;animation:marq 14s linear infinite;color:#facc15;font-weight:900;font-size:13px;letter-spacing:2px}}.lic{{background:rgba(0,0,0,.4);border:1px solid {lic_color}40;border-radius:12px;padding:10px;margin-bottom:16px}}.lic b{{color:{lic_color};font-size:11px}}.lic div{{font-size:10px;color:#94a3b8;margin-top:4px}}.copy{{margin-top:18px;font-size:10px;color:#475569}}.wa{{display:inline-block;margin-top:10px;padding:8px 16px;background:#25D366;color:#fff;border-radius:20px;font-size:11px;font-weight:800;text-decoration:none}}@keyframes marq{{0%{{transform:translate(0,0)}}100%{{transform:translate(-100%,0)}}}}input{{width:100%;margin-top:12px;padding:14px 16px;border-radius:14px;border:1px solid rgba(255,255,255,.1);background:rgba(0,0,0,.35);color:#fff}}button{{width:100%;margin-top:18px;padding:14px;border-radius:14px;border:0;background:linear-gradient(90deg,#facc15,#fde047);color:#000;font-weight:900}}</style></head><body><div class=bx><div class=marquee><span>⚡ WELCOME TO Pyrunnercloud54 ⚡ WELCOME TO Pyrunnercloud54 ⚡</span></div><div class=lg>Cloud<span>Pusat54</span></div><div class=sub>PREMIUM PANEL - ANTI RESET IP</div><div class=lic><b>{lic_text}</b><div>Owner: {own}<br>Valid Until: {exp}<br>Sisa: {dl} Hari<br>IP Ganti = Tetep Kehitung</div></div><form method=post action=/login><input name=user placeholder=admin><input name=pass type=password placeholder=cloud54><button>LOGIN PREMIUM</button></form><div class=copy><b>© 2026 CLOUDPUSAT54</b><br>Premium License - 30 Days - Anti Reset<br><a class=wa href="https://wa.me/{wa}?text=Halo%20mau%20perpanjang%20license%20Pyrunnercloud54">📱 WA: {wa}</a></div></div></body></html>'

MAIN='''<html><head><meta name=viewport content="width=device-width,initial-scale=1"><style>
*{box-sizing:border-box;font-family:Inter,system-ui}body{margin:0;background:#08070e;color:#cbd5e1;padding-bottom:110px}
.wrap{position:relative;z-index:1;max-width:480px;margin:0 auto;padding:14px}
.h{position:sticky;top:0;z-index:20;display:flex;justify-content:space-between;align-items:center;padding:14px 18px;background:rgba(8,10,18,.9);backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,255,255,.08);margin:-14px -14px 14px -14px}
.logo{font-weight:900;font-size:19px;color:#fff}.logo span{color:#facc15}
.licbar{display:flex;justify-content:space-between;align-items:center;background:linear-gradient(90deg,rgba(250,204,21,.12),rgba(250,204,21,.04));border:1px solid rgba(250,204,21,.2);border-radius:14px;padding:10px 14px;margin-bottom:14px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:rgba(255,255,255,.08);border-radius:22px;overflow:hidden;margin-bottom:18px}
.stat{background:rgba(15,15,28,.9);padding:16px}.stat b{font-size:22px;color:#fff;display:block;margin-top:4px}
.sec{background:rgba(15,15,28,.75);border:1px solid rgba(255,255,255,.08);border-radius:26px;padding:18px}
.bot{display:flex;justify-content:space-between;align-items:center;padding:14px;background:rgba(10,10,18,.6);border:1px solid rgba(255,255,255,.06);border-radius:18px;margin-top:10px}
.bot.on{border-color:rgba(250,204,21,.25);background:linear-gradient(90deg,rgba(250,204,21,.08),rgba(10,10,18,.6))}
.dot{width:9px;height:9px;border-radius:50%}.dot.on{background:#22c55e;box-shadow:0 0 10px #22c55e}.dot.off{background:#334155}
.badge{font-size:9px;padding:3px 8px;border-radius:20px;font-weight:800;border:1px solid}.badge.on{color:#4ade80;background:rgba(74,222,128,.1)}.badge.off{color:#64748b}
.btn{padding:7px 12px;border-radius:10px;border:1px solid rgba(255,255,255,.08);font-size:11px;font-weight:700;cursor:pointer}.btn-run{background:#facc15;color:#000;font-weight:900}.btn-stop{background:rgba(0,0,0,.3);color:#ef4444}.btn-log{background:rgba(0,0,0,.3);color:#94a3b8}
.inp{width:100%;padding:12px 14px;background:rgba(0,0,0,.3);border:1px solid rgba(255,255,255,.08);border-radius:12px;color:#fff;margin-bottom:10px}
.logbox{background:rgba(0,0,0,.4);border:1px solid rgba(255,255,255,.06);border-radius:12px;padding:12px;font-family:monospace;font-size:11px;max-height:300px;overflow:auto;color:#facc15;white-space:pre-wrap;margin-top:12px}
.bottom{position:fixed;bottom:14px;left:50%;transform:translateX(-50%);width:92%;max-width:400px;background:rgba(15,15,28,.95);border:1px solid rgba(255,255,255,.12);border-radius:26px;display:flex;padding:6px;z-index:9999}
.bottom div{flex:1;text-align:center;padding:14px 6px;border-radius:18px;font-size:12px;font-weight:800;color:#6b7280;cursor:pointer}.bottom div.on{background:rgba(250,204,21,.15);color:#facc15}
</style></head><body>
<div class=wrap>
<div class=h><div class=logo>Cloud<span>Pusat54</span> <span style="font-size:10px;background:rgba(250,204,21,.2);color:#facc15;padding:3px 8px;border-radius:20px">PREMIUM</span></div><div style="display:flex;gap:10px;align-items:center"><span style="font-size:11px;color:#4b5563" id="clk"></span><a href="/logout" style="color:#94a3b8;text-decoration:none;font-size:12px;border:1px solid rgba(255,255,255,.1);padding:5px 10px;border-radius:20px">Logout</a></div></div>
<div class=licbar><div><div style="font-size:10px;color:#a3a3a3">LICENSE STATUS - ANTI RESET IP</div><div style="font-size:12px;font-weight:800;color:#facc15" id="licstat">Checking...</div></div><div style="text-align:right"><div style="font-size:10px;color:#64748b">EXPIRES</div><div style="font-size:11px;color:#fff;font-weight:700" id="licexp">-</div></div></div>
<div class=grid><div class=stat><label>CPU</label><b id="cpu">-</b></div><div class=stat><label>RAM</label><b id="ram">-</b></div><div class=stat><label>DISK</label><b id="disk">-</b></div></div>
<div id="p1"><div class=sec><div style="display:flex;justify-content:space-between;margin-bottom:12px"><b style="color:#fff;font-size:13px">MY BOTS</b><span id="cnt"></span></div><div id="bots">Loading...</div><div id="rlog" class=logbox style="display:none"></div></div></div>
<div id="p2" style="display:none"><div class=sec><div id="fl"></div></div></div>
<div id="p3" style="display:none"><div class=sec><b style="color:#fff">Deploy Premium Bot</b><input id="n" class=inp placeholder="Nama bot"><input id="cmd" class=inp value="python3 main.py"><input type="file" id="z" style="margin:8px 0;color:#64748b"><button class="btn btn-run" style="width:100%;padding:13px" onclick="dp()">Deploy</button><div id="dl" class=logbox style="display:none"></div></div></div>
</div>
<div class=bottom><div id="b1" class="on" onclick="sh(1)">Monitor</div><div id="b2" onclick="sh(2)">Files</div><div id="b3" onclick="sh(3)">Deploy</div></div>
<script>
function sh(x){document.getElementById('p1').style.display=x==1?'block':'none';document.getElementById('p2').style.display=x==2?'block':'none';document.getElementById('p3').style.display=x==3?'block':'none';document.getElementById('b1').className=x==1?'on':'';document.getElementById('b2').className=x==2?'on':'';document.getElementById('b3').className=x==3?'on':'';if(x==1)lm();}
function lm(){fetch('/api/s').then(r=>r.json()).then(d=>{document.getElementById('cpu').innerText=d.c+'%';document.getElementById('ram').innerText=d.m+'GB';document.getElementById('disk').innerText=d.d+'GB';document.getElementById('licstat').innerText=d.lic_text;document.getElementById('licstat').style.color=d.lic_color;document.getElementById('licexp').innerText=d.exp;});fetch('/api/b').then(r=>r.json()).then(d=>{let h='';document.getElementById('cnt').innerText=d.length+' bots';for(let x of d){let on=x[1]=='running';h+='<div class="bot '+(on?'on':'')+'"><div style="display:flex;align-items:center;gap:11px"><div class="dot '+(on?'on':'off')+'"></div><div><div style="font-weight:700;color:#fff">'+x[0]+'</div><div style="display:flex;gap:6px;margin-top:4px"><span class="badge '+(on?'on':'off')+'">'+(on?'LIVE':'OFF')+'</span><span style="font-size:11px;color:#475569">#'+(x[2]||'0')+'</span></div></div></div><div style="display:flex;gap:5px"><button class="btn btn-run" onclick="rb(\\''+x[0]+'\\')">Run</button><button class="btn btn-stop" onclick="sb(\\''+x[0]+'\\')">Stop</button><button class="btn btn-log" onclick="lb(\\''+x[0]+'\\')">Log</button></div></div>';}document.getElementById('bots').innerHTML=h||'No bots';});}
function rb(n){document.getElementById('rlog').style.display='block';document.getElementById('rlog').innerText='Starting '+n+'...';fetch('/api/bot/'+n+'/start',{method:'POST'}).then(r=>r.json()).then(d=>{document.getElementById('rlog').innerText=d.log;lm()})}
function sb(n){fetch('/api/bot/'+n+'/stop',{method:'POST'}).then(()=>{document.getElementById('rlog').style.display='block';document.getElementById('rlog').innerText='Stopped '+n;lm()})}
function lb(n){fetch('/api/bot/'+n+'/log').then(r=>r.text()).then(t=>{document.getElementById('rlog').style.display='block';document.getElementById('rlog').innerText=t.slice(-4000)||'No log'})}
function dp(){let n=document.getElementById('n').value;if(!n)return alert('Isi nama');let fd=new FormData();fd.append('name',n);fd.append('command',document.getElementById('cmd').value);fd.append('file',document.getElementById('z').files[0]);document.getElementById('dl').style.display='block';document.getElementById('dl').innerText='Uploading...';fetch('/api/dp',{method:'POST',body:fd}).then(r=>r.json()).then(d=>{document.getElementById('dl').innerText=d.log;lm();sh(1)})}
setInterval(function(){document.getElementById('clk').innerText=new Date().toLocaleTimeString('id-ID',{hour:'2-digit',minute:'2-digit'})},1000);lm();setInterval(lm,3000);
</script></body></html>'''

@app.get('/login',response_class=HTMLResponse)
async def a():return HTMLResponse(render_login())
@app.post('/login')
async def b(user: str=Form(...),pass_: str=Form(...,alias='pass')):
 if is_expired():return HTMLResponse(f'<html><body style="background:#08070e;color:#fff;display:flex;align-items:center;justify-content:center;height:100vh;font-family:system-ui;text-align:center"><div><h1 style="color:#ef4444">⛔ LICENSE EXPIRED</h1><p>30 Days License Habis - Hubungi CLOUDPUSAT54</p><p>Expired: {get_expiry().strftime("%d %B %Y")}</p><a href="https://wa.me/{WA_NUMBER}?text=Halo%20license%20habis%20mau%20perpanjang" style="display:inline-block;margin-top:12px;padding:10px 20px;background:#25D366;color:#fff;border-radius:20px;text-decoration:none;font-weight:800">📱 Chat WA {WA_NUMBER}</a><br><br><a href="/login" style="color:#facc15">Back</a></div></body></html>',401)
 if user=='admin' and hashlib.sha256((pass_+S).encode()).hexdigest()==P:
  r=RedirectResponse('/',302);r.set_cookie('auth',P,max_age=86400*30,httponly=True);return r
 return HTMLResponse(render_login(),401)
@app.get('/logout')
async def c():r=RedirectResponse('/login',302);r.delete_cookie('auth');return r
@app.get('/',response_class=HTMLResponse)
async def d(request: Request):
 if not ok(request):return RedirectResponse('/login',302)
 if is_expired():return HTMLResponse(f'<html><body style="background:#08070e;color:#fff;display:flex;align-items:center;justify-content:center;height:100vh;text-align:center"><div><h1 style="color:#ef4444">⛔ LICENSE EXPIRED - 30 DAYS HABIS</h1><p>Hubungi CLOUDPUSAT54 untuk perpanjang - License tetep kehitung walau ganti IP</p><p>Expired: {get_expiry().strftime("%d %B %Y")}</p><a href="https://wa.me/{WA_NUMBER}?text=Halo%20license%20habis%20mau%20perpanjang" style="display:inline-block;margin-top:12px;padding:10px 20px;background:#25D366;color:#fff;border-radius:20px;text-decoration:none">📱 WA {WA_NUMBER}</a><br><br><a href="/logout" style="color:#facc15">Logout</a></div></body></html>')
 return HTMLResponse(MAIN)
@app.get('/api/b')
async def e():
 o=[]
 for n in os.listdir(B):
  p=os.path.join(B,n)
  if os.path.isdir(p) and not n.startswith('.'):
   run,pid=is_run(p,n);auto=os.path.exists(os.path.join(p,'.autorun'));o.append([n,'running' if run else 'stopped',pid,auto])
 return JSONResponse(sorted(o))
@app.post('/api/bot/{name}/start')
async def f(name: str):
 if is_expired():return JSONResponse({'log':'⛔ LICENSE EXPIRED - Hubungi WA 6285218016760'})
 bp=os.path.join(B,name);auto_fix_bot(bp)
 for pr in psutil.process_iter(['pid']):
  try:
   if pr.cwd()==bp:pr.kill()
  except:pass
 time.sleep(0.5);pid=start_bot_process(bp);time.sleep(1.5);run,pid2=is_run(bp,name)
 log=""
 try:log=open(os.path.join(bp,'bot.log'),errors='ignore').read()[-2000:]
 except:pass
 if run:open(os.path.join(bp,'.autorun'),'w').write('1');return JSONResponse({'log':f'✅ LIVE {name} PID {pid2}\nLicense: {days_left()} hari lagi - Anti Reset IP\n{log}'})
 else:return JSONResponse({'log':f'⚠️ TRY {name} - Auto retry 30s\nLicense: {days_left()} hari\n{log}'})
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
 if is_expired():return JSONResponse({'ok':False,'log':'LICENSE EXPIRED'})
 f=await request.form();na=f.get('name');fi=f.get('file');de=os.path.join(B,na);os.makedirs(de,exist_ok=True)
 log=f"Deploy {na}\nLicense: {days_left()} hari lagi - Anti Reset IP\n"
 if fi:
  da=await fi.read();zp=os.path.join(de,'a.zip');open(zp,'wb').write(da)
  try:
   with zipfile.ZipFile(zp,'r') as z:z.extractall(de);log+=f"Extract OK\n"
  except Exception as e:log+=f"Fail {e}\n"
  try:os.remove(zp)
  except:pass
 open(os.path.join(de,'.command'),'w').write(f.get('command') or 'python3 main.py')
 auto_fix_bot(de)
 return JSONResponse({'ok':True,'log':log})
@app.get('/api/s')
async def o():
 dl=days_left();exp=get_expiry().strftime('%d %b %Y')
 if dl>10:lc="#4ade80";lt=f"ACTIVE - {dl} HARI LAGI"
 elif dl>3:lc="#facc15";lt=f"WARNING - {dl} HARI LAGI"
 elif dl>=0:lc="#fb923c";lt=f"SEGERA HABIS - {dl} HARI!"
 else:lc="#ef4444";lt="EXPIRED!"
 return JSONResponse({'c':round(psutil.cpu_percent(),1),'m':round(psutil.virtual_memory().used/1024/1024/1024,1),'d':round(psutil.disk_usage('/').used/1024/1024/1024,1),'lic_text':lt,'lic_color':lc,'exp':exp,'days':dl})
