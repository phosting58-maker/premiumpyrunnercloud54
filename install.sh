#!/bin/bash
set -e
echo "=========================================="
echo "  CloudPusat54 PREMIUM V12 AUTO-FIX"
echo "  WELCOME TO Pyrunnercloud54"
echo "=========================================="
apt update -y
apt install -y python3-venv python3-pip curl wget git zip unzip psmisc -y
mkdir -p /root/panel /root/apps
python3 -m venv /root/panel-venv
/root/panel-venv/bin/pip install fastapi uvicorn psutil python-multipart telethon --quiet --upgrade
echo "Downloading Premium V12..."
wget -qO /root/panel/app.py https://raw.githubusercontent.com/phosting58-maker/premiumpyrunnercloud54/main/app.py
if [ ! -s /root/panel/app.py ]; then echo "Gagal download app.py!"; exit 1; fi
cat > /etc/systemd/system/cloud54.service << 'SVC'
[Unit]
Description=CloudPusat54 Premium V12 Auto-Fix
After=network.target
[Service]
User=root
WorkingDirectory=/root/panel
ExecStart=/root/panel-venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3
[Install]
WantedBy=multi-user.target
SVC
systemctl daemon-reload
systemctl enable cloud54
systemctl restart cloud54
sleep 2
IP=$(curl -s ifconfig.me || hostname -I | awk '{print $1}')
echo ""
echo "=========================================="
echo "✅ PREMIUM V12 INSTALLED!"
echo "Panel: http://$IP:8000"
echo "Login: admin / cloud54"
echo "Tampilan: WELCOME TO Pyrunnercloud54 berjalan"
echo "Copyright: © 2026 CLOUDPUSAT54"
echo "Fitur: AUTO-FIX Wtfplto_bot & semua bot"
echo "Repo: premiumpyrunnercloud54"
echo "=========================================="