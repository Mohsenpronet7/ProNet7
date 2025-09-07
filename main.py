import requests
import base64
import jdatetime

# تابع برای چک کردن اینکه متن base64 هست یا نه
def is_base64(s: str) -> bool:
    try:
        return base64.b64encode(base64.b64decode(s)).decode().strip() == s.strip()
    except Exception:
        return False

# فایل ورودی لیست لینک‌ها
with open("sources.txt", "r") as f:
    urls = [line.strip() for line in f if line.strip()]

all_configs = []
for url in urls:
    try:
        res = requests.get(url, timeout=20)
        if res.status_code == 200:
            text = res.text.strip()

            if is_base64(text.replace("\n", "")):  # اگر base64 بود
                decoded = base64.b64decode(text).decode("utf-8", errors="ignore")
                configs = [line.strip() for line in decoded.splitlines() if line.strip()]
            else:  # اگر نبود
                configs = [line.strip() for line in text.splitlines() if line.strip()]

            all_configs.extend(configs)

    except Exception as e:
        print(f"خطا در دریافت {url}: {e}")

# حذف تکراری‌ها
unique_configs = list(dict.fromkeys(all_configs))

# تاریخ و ساعت شمسی
now = jdatetime.datetime.now().strftime("%d %B %Y ساعت %H:%M")

# ذخیره فایل خروجی txt
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(unique_configs))

# ساخت HTML شکیل‌تر
html_content = f"""
<!DOCTYPE html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <title>📡 لیست سرورهای V2Ray</title>
    <style>
        body {{
            font-family: Vazirmatn, Tahoma, sans-serif;
            background: #f5f7fa;
            color: #222;
            text-align: center;
            padding: 40px;
        }}
        h2 {{
            color: #2c3e50;
        }}
        .info {{
            margin: 20px 0;
            font-size: 18px;
        }}
        .btn {{
            display: inline-block;
            margin: 20px;
            padding: 12px 24px;
            background: #27ae60;
            color: #fff;
            text-decoration: none;
            border-radius: 8px;
            font-size: 16px;
            transition: 0.3s;
        }}
        .btn:hover {{
            background: #2ecc71;
        }}
        pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 20px;
            border-radius: 10px;
            text-align: left;
            direction: ltr;
            overflow-x: auto;
            max-height: 500px;
        }}
    </style>
</head>
<body>
    <h2>📡 لیست سرورهای V2Ray</h2>
    <div class="info">📅 بروزرسانی: {now} به وقت تهران</div>
    <div class="info">🔗 تعداد سرورها: {len(unique_configs)}</div>
    <a class="btn" href="output.txt" download>⬇️ دانلود فایل کامل (output.txt)</a>
    <pre>{chr(10).join(unique_configs[:50])}</pre>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
