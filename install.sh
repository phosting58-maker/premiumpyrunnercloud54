#!/bin/bash
set -e
echo "== CloudPusat54 PREMIUM - ANTI RESET IP =="
mkdir -p /root/panel /root/apps

# CEK BACKUP LICENSE DI 3 TEMPAT - KALO ADA, RESTORE!
if [ -f /root/panel/.install_date ]; then
  echo "✅ License lama ada: $(cat /root/panel/.install_date)"
elif [ -f /root/.license_backup ]; then
  cp /root/.license_backup /root/panel/.install_date
  echo "✅ Restore dari backup root: $(cat /root/panel/.install_date)"
elif [ -f /root/apps/.license_backup ]; then
  cp /root/apps/.license_backup /root/panel/.install_date
  echo "✅ Restore dari backup apps: $(cat /root/panel/.install_date)"
else
  date +%Y-%m-%d > /root/panel/.install_date
  echo "🆕 NEW LICENSE: $(cat /root/panel/.install_date) -> 30 Days"
fi

# BACKUP KE 2 TEMPAT BIAR GANTI IP AMAN
cp /root/panel/.install_date /root/.license_backup
cp /root/panel/.install_date /root/apps/.license_backup
EXPIRE=$(date -d "$(cat /root/panel/.install_date) +30 days" +%d\ %B\ %Y)
echo "Expire: $EXPIRE"

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
echo "=========================================="
echo "✅ INSTALLED ANTI RESET IP!"
echo "Panel: http://$IP:8000"
echo "License: $(cat /root/panel/.install_date) - $EXPIRE"
echo "IP ganti pun sisa hari tetep!"
echo "=========================================="
