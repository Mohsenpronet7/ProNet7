import requests
import base64
import jdatetime
from datetime import datetime
import pytz
import qrcode
from io import BytesIO
import base64 as b64

# لینک مورد نظر برای QR کد
v2ray_link = "https://mohsenpronet7.github.io/ProNet7/output.txt"

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

# ذخیره فایل خروجی txt
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(unique_configs))

# تولید QR کد و تبدیل به Base64 برای نمایش در HTML
qr = qrcode.QRCode(box_size=6, border=2)
qr.add_data(v2ray_link)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")

buffered = BytesIO()
img.save(buffered, format="PNG")
img_str = b64.b64encode(buffered.getvalue()).decode()

# ساخت HTML شکیل‌تر با QR
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
        .qr {{
            margin: 30px 0;
        }}
    </style>
</head>
<body>
    <h2>📡 لیست سرورهای V2Ray</h2>
    <div class="info">📅 بروزرسانی: {now} به وقت تهران</div>
    <div class="info">🔗 تعداد سرورها: {len(unique_configs)}</div>
    <a class="btn" href="output.txt" download>⬇️ دانلود فایل کامل (output.txt)</a>
    <div class="qr">
        <h3>📱 اسکن QR برای استفاده در V2RayNG / Hiddify</h3>
        <img src="data:image/png;base64,{img_str}" alt="QR Code">
    </div>
    <pre>{chr(10).join(unique_configs[:50])}</pre>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
