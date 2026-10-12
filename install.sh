#!/bin/bash
set -e
echo "== CloudPusat54 PREMIUM - 30 DAYS =="
mkdir -p /root/panel /root/apps
date +%Y-%m-%d > /root/panel/.install_date
echo "License: 30 Days $(cat /root/panel/.install_date) -> $(date -d '+30 days' +%Y-%m-%d)"
python3 -m venv /root/panel-venv 2>/dev/null || true
/root/panel-venv/bin/pip install fastapi uvicorn psutil python-multipart telethon -q --no-cache-dir
wget -qO /root/panel/app.py https://raw.githubusercontent.com/phosting58-maker/premiumpyrunnercloud54/main/app.py
cat > /etc/systemd/system/cloud54.service << 'SVC'
[Unit]
Description=CloudPusat54 Premium
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
systemctl daemon-reload; systemctl enable cloud54; systemctl restart cloud54
IP=$(curl -s ifconfig.me)
echo "✅ PREMIUM 30 DAYS INSTALLED! http://$IP:8000"
