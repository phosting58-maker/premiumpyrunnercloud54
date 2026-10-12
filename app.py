# HAPUS YANG RUSAK
rm /root/panel/app.py

# INSTALL ULTRA MINIMAL DULU BIAR NYALA (29 HARI TETEP)
cat > /root/panel/app.py << 'PYEOF'
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
import os, psutil, subprocess, hashlib, zipfile, pathlib, time, glob, threading, datetime, shutil
app=FastAPI(docs_url=None, redoc_url=None)
B='/root/apps';os.makedirs(B,exist_ok=True)
S='cloudpusat54';P=hashlib.sha256(('cloud54'+S).encode()).hexdigest()
INSTALL_FILE='/root/panel/.install_date'
BACKUP1='/root/.license_backup'
BACKUP2='/root/apps/.license_backup'
WA='6285218016760'
def get_install_date():
    try:
        for p in [INSTALL_FILE,BACKUP1,BACKUP2]:
            if os.path.exists(p):
                d=open(p).read().strip()
                if d:
                    try:
                        os.makedirs('/root/panel',exist_ok=True)
                        open(INSTALL_FILE,'w').write(d)
                        open(BACKUP1,'w').write(d)
                        open(BACKUP2,'w').write(d)
                    except: pass
                    return datetime.datetime.strptime(d,'%Y-%m-%d')
        now=datetime.datetime.now().strftime('%Y-%m-%d')
        os.makedirs('/root/panel',exist_ok=True)
        open(INSTALL_FILE,'w').write(now)
        open(BACKUP1,'w').write(now)
        open(BACKUP2,'w').write(now)
        return datetime.datetime.strptime(now,'%Y-%m-%d')
    except:
        return datetime.datetime.now()
def get_expiry():
    return get_install_date()+datetime.timedelta(days=30)
def days_left():
    return (get_expiry()-datetime.datetime.now()).days
def ok(r):
    return r.cookies.get('auth','')==P
def is_run(bp,bn):
    pf=os.path.join(bp,'.pid')
    if os.path.exists(pf):
        try:
            pid=int(open(pf).read().strip() or "0")
            if pid and psutil.pid_exists(pid):
                return True, pid
        except:
            pass
    return False, 0
def start_bot_process(bp):
    cf=os.path.join(bp,'.command')
    if os.path.exists(cf):
        cmd=pathlib.Path(cf).read_text().strip()
    else:
        cmd='python3 main.py'
    full=f"cd {bp} && nohup {cmd} > bot.log 2>&1 & echo $!"
    r=subprocess.run(full,shell=True,capture_output=True,text=True,timeout=10)
    return r.stdout.strip()
@app.get('/login',response_class=HTMLResponse)
async def login_page():
    exp=get_expiry().strftime('%d %B %Y');dl=days_left()
    return HTMLResponse(f"<html><body style='background:#08070e;color:#fff;font-family:system-ui;display:flex;align-items:center;justify-content:center;height:100vh'><div><h2>CloudPusat54 PREMIUM {dl} HARI - Expire {exp}</h2><form method=post action=/login><input name=user placeholder=admin><input name=pass type=password placeholder=cloud54><button>LOGIN</button></form></div></body></html>")
@app.post('/login')
async def login_post(user: str=Form(...), pass_: str=Form(..., alias='pass')):
    if user=='admin' and hashlib.sha256((pass_+S).encode()).hexdigest()==P:
        r=RedirectResponse('/',302);r.set_cookie('auth',P,max_age=86400*30);return r
    return HTMLResponse("fail",401)
@app.get('/',response_class=HTMLResponse)
async def home(request: Request):
    if not ok(request):
        return RedirectResponse('/login',302)
    dl=days_left();exp=get_expiry().strftime('%d %B %Y')
    return HTMLResponse(f"<html><body style='background:#08070e;color:#fff;padding:20px'><h2>RECOVERY MODE - ACTIVE {dl} HARI</h2><p>Expire: {exp}</p><p>IP: 139.59.101.177 - Anti Reset IP OK</p><p>Panel nyala! Sekarang update ke versi full file manager</p><a href='/login'>login</a></body></html>")
@app.get('/api/b')
async def api_b():
    o=[]
    for n in os.listdir(B):
        p=os.path.join(B,n)
        if os.path.isdir(p) and not n.startswith('.'):
            o.append([n,'stopped',0])
    return JSONResponse(o)
PYEOF

/root/panel-venv/bin/pip install fastapi uvicorn psutil -q
systemctl daemon-reload
systemctl restart cloud54
sleep 2
systemctl status cloud54 --no-pager | head -20
echo "=== PANEL HARUSNYA NYALA ==="
curl -s http://127.0.0.1:8000/ | head -20
