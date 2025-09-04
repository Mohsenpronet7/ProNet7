import requests
import base64
from datetime import datetime
from zoneinfo import ZoneInfo  # استاندارد پایتون 3.9+
import jdatetime

# --- ابزارهای کمکی ---
def b64decode_loose(s: str) -> str:
    """برخی سابسکریپشن‌ها padding ندارند؛ این تابع با اضافه کردن '=' دیکد می‌کند."""
    s = s.strip()
    # اگر متن خام باشد (مثلاً vmess://...) هم همان را برمی‌گردانیم
    try:
        missing = len(s) % 4
        if missing:
            s += "=" * (4 - missing)
        return base64.b64decode(s).decode("utf-8", errors="ignore")
    except Exception:
        return s  # متن خام

def to_persian_digits(x: str) -> str:
    trans = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
    return str(x).translate(trans)

MONTHS_FA = {
    1:"فروردین",2:"اردیبهشت",3:"خرداد",4:"تیر",5:"مرداد",6:"شهریور",
    7:"مهر",8:"آبان",9:"آذر",10:"دی",11:"بهمن",12:"اسفند"
}

def tehran_now_jalali_str() -> str:
    """نمونه خروجی: ۱۳ شهریور ۱۴۰۴ ساعت ۲۱:۴۳"""
    g_now = datetime.now(ZoneInfo("Asia/Tehran"))
    j_now = jdatetime.datetime.fromgregorian(datetime=g_now)
    day = to_persian_digits(j_now.day)
    month = MONTHS_FA[j_now.month]
    year = to_persian_digits(j_now.year)
    hm = to_persian_digits(g_now.strftime("%H:%M"))
    return f"{day} {month} {year} ساعت {hm}"

# --- خواندن لینک‌ها ---
with open("sources.txt", "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]

all_configs = []

for url in urls:
    try:
        r = requests.get(url, timeout=25)
        if r.status_code == 200 and r.text.strip():
            decoded = b64decode_loose(r.text)
            lines = [ln.strip() for ln in decoded.splitlines() if ln.strip()]
            all_configs.extend(lines)
    except Exception as e:
        print(f"خطا در دریافت {url}: {e}")

# حذف تکراری‌ها با حفظ ترتیب
unique_configs = list(dict.fromkeys(all_configs))

# تاریخ/ساعت به وقت تهران و فارسی
now_fa = tehran_now_jalali_str()

# ذخیره فایل خروجی txt (فقط لیست)
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(unique_configs))

# HTML شکیل
html = f"""<!DOCTYPE html>
<html lang="fa">
<head>
  <meta charset="utf-8">
  <title>سرورهای V2Ray</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <style>
    body {{
      font-family: Tahoma, Arial, sans-serif;
      background:#f9fafb; margin:0; padding:24px; direction:rtl; text-align:center;
    }}
    .card {{
      background:#fff; max-width:900px; margin:auto; padding:24px;
      border-radius:16px; box-shadow:0 6px 18px rgba(0,0,0,.08);
    }}
    h1 {{ margin:0 0 8px; color:#0f172a; font-size:22px; }}
    .muted {{ color:#334155; margin:6px 0; }}
    .count {{ font-weight:bold; }}
    .btn {{
      display:inline-block; margin:16px 0; padding:10px 18px; border-radius:10px;
      background:#16a34a; color:#fff; text-decoration:none; font-weight:700;
    }}
    textarea {{
      width:100%; height:420px; margin-top:12px; padding:12px; border-radius:12px;
      border:1px solid #cbd5e1; font-family:monospace; direction:ltr; font-size:13px;
    }}
    footer {{ margin-top:14px; color:#64748b; font-size:12px; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>📡 لیست سرورهای V2Ray</h1>
    <p class="muted">📅 بروزرسانی: {now_fa} به وقت تهران</p>
    <p class="muted">🔗 تعداد سرورها: <span class="count">{to_persian_digits(len(unique_configs))}</span></p>
    <a class="btn" href="output.txt" download>⬇️ دانلود فایل کامل (output.txt)</a>
    <textarea readonly>{"\n".join(unique_configs[:200])}</textarea>
    <footer>(برای نمایش سریع، فقط ۲۰۰ سرور اول اینجاست؛ همه‌ی سرورها داخل فایل output.txt هستند)</footer>
  </div>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
