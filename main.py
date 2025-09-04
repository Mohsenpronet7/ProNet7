import requests
import base64
from datetime import datetime
import jdatetime

# فایل ورودی لیست لینک‌ها
with open("sources.txt", "r") as f:
    urls = [line.strip() for line in f if line.strip()]

all_configs = []

for url in urls:
    try:
        res = requests.get(url, timeout=20)
        if res.status_code == 200:
            decoded = base64.b64decode(res.text).decode("utf-8", errors="ignore")
            configs = [line.strip() for line in decoded.splitlines() if line.strip()]
            all_configs.extend(configs)
    except Exception as e:
        print(f"خطا در دریافت {url}: {e}")

# حذف تکراری‌ها
unique_configs = list(dict.fromkeys(all_configs))

# تاریخ و ساعت شمسی
now = jdatetime.datetime.now().strftime("%d %B %Y ساعت %H:%M")

# ساخت متن خروجی
header = f"# بروزرسانی: {now}\n\n"
output = header + "\n".join(unique_configs)

# ذخیره فایل خروجی txt
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(output)

# ساخت فایل index.html برای GitHub Pages
html_content = f"""
<html>
<head><meta charset="utf-8"><title>سرورها</title></head>
<body>
<h2>آخرین {len(unique_configs)} سرور جمع‌آوری‌شده</h2>
<p>بروزرسانی: {now} به وقت تهران</p>
<textarea style="width:100%;height:400px;">{"\n".join(unique_configs)}</textarea>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
