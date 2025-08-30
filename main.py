import base64
import requests
import socket
import jdatetime
import pytz
from datetime import datetime

# فایل منابع لینک‌ها
with open("sources.txt") as f:
    sources = [line.strip() for line in f if line.strip()]

all_nodes = set()

def fetch_and_decode(url):
    try:
        resp = requests.get(url, timeout=15)
        data = base64.b64decode(resp.text.strip()).decode(errors="ignore")
        return [line.strip() for line in data.splitlines() if line.strip()]
    except Exception as e:
        print(f"[!] Error fetching {url}: {e}")
        return []

# تست سلامت (ping ساده با TCP)
def is_alive(node):
    try:
        if node.startswith("vmess://"):
            payload = base64.b64decode(node.replace("vmess://", "")).decode(errors="ignore")
            import json
            info = json.loads(payload)
            host, port = info.get("add"), int(info.get("port", 443))
        elif node.startswith("ss://") or node.startswith("trojan://"):
            rest = node.split("@")[1]
            host, port = rest.split(":")[0], int(rest.split(":")[1].split("#")[0])
        else:
            return False
        s = socket.socket()
        s.settimeout(2)
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False

# جمع‌آوری سرورها
for url in sources:
    nodes = fetch_and_decode(url)
    for n in nodes:
        all_nodes.add(n)

print(f"[+] Total nodes before filter: {len(all_nodes)}")

# تست و فیلتر سالم‌ها
alive_nodes = [n for n in all_nodes if is_alive(n)]
print(f"[+] Alive nodes: {len(alive_nodes)}")

# ساخت خروجی subscription
final_str = "\n".join(alive_nodes)
encoded = base64.b64encode(final_str.encode()).decode()

with open("output.txt", "w") as f:
    f.write(encoded)

# زمان فعلی به وقت تهران (شمسی)
tehran = pytz.timezone("Asia/Tehran")
now_tehran = datetime.now(tehran)
jnow = jdatetime.datetime.fromgregorian(datetime=now_tehran)
formatted_time = f"آپدیت: {jnow.day} {jnow.j_months_fa[jnow.month-1]} {jnow.year} ساعت {now_tehran.strftime('%H:%M')} به وقت تهران"

# ساخت صفحه HTML ساده
html = f"""
<!DOCTYPE html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <title>V2Ray Subscription</title>
    <style>
        body {{ font-family: sans-serif; direction: rtl; max-width: 600px; margin: auto; padding: 20px; }}
        .card {{ background: #f9f9f9; padding: 20px; border-radius: 12px; box-shadow: 0 0 8px rgba(0,0,0,0.1); }}
        h1 {{ font-size: 1.5rem; }}
        .meta {{ color: #555; margin-bottom: 10px; }}
        a {{ display: inline-block; margin-top: 10px; padding: 10px 15px; background: #007bff; color: #fff; border-radius: 8px; text-decoration: none; }}
        a:hover {{ background: #0056b3; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>V2Ray Subscription</h1>
        <div class="meta">{formatted_time}</div>
        <div>تعداد سرورهای سالم: {len(alive_nodes)}</div>
        <a href="output.txt">دانلود سابسکریپشن</a>
    </div>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html)

print("[+] Files generated: output.txt & index.html")