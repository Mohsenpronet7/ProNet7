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

# تاریخ و ساعت شمسی (به فارسی)
months_fa = [
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
    "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
]
now_jalali = jdatetime.datetime.now()
now_fa = f"{now_jalali.day} {months_fa[now_jalali.month - 1]} {now_jalali.year} ساعت {now_jalali.strftime('%H:%M')}"

# ذخیره فایل خروجی txt
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(unique_configs))

# ساخت HTML شکیل‌تر با رنگ صورتی + سفید
html_content = f"""
<!DOCTYPE html>
<html lang="fa">
<head>
  <meta charset="UTF-8">
  <title>📡 لیست سرورهای V2Ray</title>
  <style>
    body {{
      font-family: Tahoma, Arial, sans-serif;
      background: linear-gradient(135deg, #ffe6f0, #ffffff);
      color: #333;
      text-align: center;
      padding: 30px;
    }}
    h2 {{
      color: #cc0066;
    }}
    .info {{
      margin: 15px 0;
      font-size: 18px;
    }}
    .btn {{
      display: inline-block;
      margin: 20px 0;
      padding: 12px 25px;
      font-size: 16px;
      color: white;
      background: #ff6699;
      border-radius: 8px;
      text-decoration: none;
      transition: background 0.3s;
    }}
    .btn:hover {{
      background: #ff3366;
    }}
    textarea {{
      width: 95%;
      height: 400px;
      margin-top: 20px;
      padding: 10px;
      border: 1px solid #ddd;
      border-radius: 8px;
      background: #fff0f5;
      font-size: 13px;
      direction: ltr;
    }}
  </style>
</head>
<body>
  <h2>📡 لیست سرورهای V2Ray</h2>
  <div class="info">📅 بروزرسانی: {now_fa} به وقت تهران</div>
  <div class="info">🔗 تعداد سرورها: {len(unique_configs)}</div>
  <a href="output.txt" class="btn">⬇️ دانلود فایل کامل (output.txt)</a>
  <textarea readonly>{"\\n".join(unique_configs[:50])}</textarea>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
