import requests
import base64
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

# ذخیره فایل خروجی txt
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(unique_configs))

# ساخت HTML شکیل‌تر
html_content = f"""
<!DOCTYPE html>
<html lang="fa">
<head>
    <meta charset="utf-8">
    <title>📡 لیست سرورهای V2Ray</title>
    <style>
        body {{
            font-family: Tahoma, Arial, sans-serif;
            direction: rtl;
            text-align: center;
            background: #f4f6f9;
            margin: 0;
            padding: 20px;
        }}
        h1 {{
            color: #2c3e50;
        }}
        .info {{
            margin: 20px auto;
            font-size: 18px;
            background: #fff;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            max-width: 600px;
        }}
        a {{
            display: inline-block;
            margin-top: 10px;
            padding: 10px 20px;
            background: #3498db;
            color: #fff;
            text-decoration: none;
            border-radius: 8px;
            transition: 0.3s;
        }}
        a:hover {{
            background: #2980b9;
        }}
        textarea {{
            width: 90%;
            height: 400px;
            margin-top: 20px;
            padding: 10px;
            font-size: 13px;
            direction: ltr;
        }}
    </style>
</head>
<body>
    <h1>📡 لیست سرورهای V2Ray</h1>
    <div class="info">
        <p>📅 بروزرسانی: {now} به وقت تهران</p>
        <p>🔗 تعداد سرورها: {len(unique_configs)}</p>
        <a href="output.txt" download>⬇️ دانلود فایل کامل (output.txt)</a>
    </div>
    <textarea readonly>
{chr(10).join(unique_configs[:200])}
    </textarea>
    <p style="color:gray; font-size:14px;">(فقط ۲۰۰ سرور اول برای نمایش سریع لیست شده‌اند)</p>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
