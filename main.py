import requests
import base64
import jdatetime
from datetime import datetime
import pytz

# فایل ورودی لیست لینک‌ها
with open("sources.txt", "r") as f:
    urls = [line.strip() for line in f if line.strip()]

# تابع برای چک کردن اینکه متن base64 هست یا نه
def is_base64(s: str) -> bool:
    try:
        return base64.b64encode(base64.b64decode(s)).decode().strip() == s.strip()
    except Exception:
        return False

all_configs = []
for url in urls:
    try:
        res = requests.get(url, timeout=20)
        if res.status_code == 200:
            text = res.text.strip()

            if is_base64(text.replace("\n", "")):
                decoded = base64.b64decode(text).decode("utf-8", errors="ignore")
                configs = [line.strip() for line in decoded.splitlines() if line.strip()]
            else:
                configs = [line.strip() for line in text.splitlines() if line.strip()]

            all_configs.extend(configs)
    except Exception as e:
        print(f"خطا در دریافت {url}: {e}")

# حذف تکراری‌ها
unique_configs = list(dict.fromkeys(all_configs))

# تاریخ و ساعت شمسی با timezone ایران
tehran_tz = pytz.timezone("Asia/Tehran")
now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
now_tehran = now_utc.astimezone(tehran_tz)
now_jalali = jdatetime.datetime.fromgregorian(datetime=now_tehran)

# دیکشنری نام ماه فارسی
months_fa = {
    1: "فروردین", 2: "اردیبهشت", 3: "خرداد", 4: "تیر",
    5: "مرداد", 6: "شهریور", 7: "مهر", 8: "آبان",
    9: "آذر", 10: "دی", 11: "بهمن", 12: "اسفند"
}

now = f"{now_jalali.day} {months_fa[now_jalali.month]} {now_jalali.year} ساعت {now_jalali.hour:02}:{now_jalali.minute:02}"

# ذخیره فایل خروجی txt با اسم جدید
with open("Mohsen_Pronet7.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(unique_configs))

# مسیر تصویر QR که کنار پروژه باشد
qr_image_path = "qr.png"

# ساخت HTML شکیل با تصویر QR سایز استاندارد ۲۰۰x۲۰۰
html_content = f"""
<!DOCTYPE html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <title>📡 لیست سرورهای V2Ray</title>
    <style>
        body {{
            font-family: Vazirmatn, Tahoma, Arial, sans-serif;
            background: linear-gradient(135deg, #ffe6f0, #ffffff);
            color: #222;
            text-align: center;
            padding: 40px;
        }}
        h2 {{
            color: #c2185b;
        }}
        .info {{
            margin: 20px 0;
            font-size: 18px;
        }}
        .btn {{
            display: inline-block;
            margin: 20px;
            padding: 12px 24px;
            background: #d81b60;
            color: #fff;
            text-decoration: none;
            border-radius: 8px;
            font-size: 16px;
            transition: 0.3s;
        }}
        .btn:hover {{
            background: #ec407a;
        }}
        pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 10px;
            text-align: left;
            direction: ltr;
            unicode-bidi: plaintext;
            font-family: Vazirmatn, Tahoma, Arial, sans-serif;
            font-size: 14px;
            overflow-x: auto;
            max-height: 500px;
        }}
        .qr {{
            margin: 30px 0;
        }}
        .qr img {{
            width: 200px;
            height: 200px;
        }}
    </style>
</head>
<body>
    <h2>📡 لیست سرورهای V2Ray</h2>
    <div class="info">📅 بروزرسانی: {now} به وقت تهران</div>
    <div class="info">🔗 تعداد سرورها: {len(unique_configs)}</div>
    <a class="btn" href="Mohsen_Pronet7.txt" download>⬇️ دانلود فایل کامل (Mohsen_Pronet7.txt)</a>
    <div class="qr">
        <h3>📱 اسکن QR برای استفاده در V2RayNG / Hiddify</h3>
        <img src="{qr_image_path}" alt="QR Code">
    </div>
    <pre>{chr(10).join(unique_configs[:50])}</pre>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
