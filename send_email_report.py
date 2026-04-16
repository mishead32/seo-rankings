#!/usr/bin/env python3
"""
Daily SEO Email Report
Sends beautiful HTML email with rankings for all 3 brands.
From: mis.gcs1@gmail.com  →  To: rajsinghrana45@gmail.com
Time: 9 AM IST (triggered by GitHub Actions)
"""
import json, os, smtplib, sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timezone, timedelta

SENDER    = os.environ.get("GMAIL_SENDER",   "mis.gcs1@gmail.com")
PASSWORD  = os.environ.get("GMAIL_PASSWORD", "")
RECIPIENT = os.environ.get("GMAIL_TO",       "rajsinghrana45@gmail.com")
IST       = timedelta(hours=5, minutes=30)


def rank_badge(r):
    if r is None:
        return '<span style="color:#cbd5e1;font-size:15px">—</span>'
    if r <= 3:
        bg, fg = "#dcfce7", "#15803d"
    elif r <= 10:
        bg, fg = "#fef9c3", "#a16207"
    else:
        bg, fg = "#fee2e2", "#dc2626"
    return (f'<span style="background:{bg};color:{fg};font-weight:700;'
            f'padding:3px 10px;border-radius:6px;font-size:13px">#{r}</span>')


def brand_block(name, data):
    kws   = data.get("keywords", [])
    total = len(kws)
    top3  = sum(1 for k in kws if k.get("rank") and k["rank"] <= 3)
    top10 = sum(1 for k in kws if k.get("rank") and k["rank"] <= 10)
    miss  = sum(1 for k in kws if not k.get("rank"))
    color = data.get("color", "#2563eb")

    rows = ""
    for i, k in enumerate(kws):
        bg = "#f8fafc" if i % 2 == 0 else "#ffffff"
        rows += f"""
        <tr style="background:{bg}">
          <td style="padding:9px 14px;color:#94a3b8;font-size:12px;width:36px">{i+1}</td>
          <td style="padding:9px 14px;color:#334155;font-size:13px">{k['keyword']}</td>
          <td style="padding:9px 14px;text-align:center">{rank_badge(k.get('rank'))}</td>
        </tr>"""

    return f"""
  <div style="margin-bottom:36px;background:#fff;border-radius:14px;
              border:1px solid #e2e8f0;overflow:hidden;
              box-shadow:0 2px 8px rgba(0,0,0,.06)">

    <!-- Brand header -->
    <div style="background:linear-gradient(90deg,{color}15,{color}05);
                border-left:5px solid {color};padding:18px 24px">
      <h2 style="margin:0;font-size:17px;font-weight:700;color:#1e293b">{name}</h2>
      <p style="margin:4px 0 0;font-size:12px;color:#64748b">
        🌐 {data.get('website','')}
      </p>
    </div>

    <!-- Summary cards -->
    <div style="display:flex;gap:0;border-bottom:1px solid #f1f5f9">
      <div style="flex:1;padding:14px 18px;border-right:1px solid #f1f5f9;text-align:center">
        <div style="font-size:10px;color:#94a3b8;text-transform:uppercase;
                    letter-spacing:.06em;font-weight:600">Total</div>
        <div style="font-size:26px;font-weight:800;color:#1e293b">{total}</div>
      </div>
      <div style="flex:1;padding:14px 18px;border-right:1px solid #f1f5f9;text-align:center">
        <div style="font-size:10px;color:#94a3b8;text-transform:uppercase;
                    letter-spacing:.06em;font-weight:600">🟢 Top 3</div>
        <div style="font-size:26px;font-weight:800;color:#15803d">{top3}</div>
      </div>
      <div style="flex:1;padding:14px 18px;border-right:1px solid #f1f5f9;text-align:center">
        <div style="font-size:10px;color:#94a3b8;text-transform:uppercase;
                    letter-spacing:.06em;font-weight:600">🟡 Page 1</div>
        <div style="font-size:26px;font-weight:800;color:#d97706">{top10}</div>
      </div>
      <div style="flex:1;padding:14px 18px;text-align:center">
        <div style="font-size:10px;color:#94a3b8;text-transform:uppercase;
                    letter-spacing:.06em;font-weight:600">🔴 Not Top 10</div>
        <div style="font-size:26px;font-weight:800;color:#dc2626">{miss}</div>
      </div>
    </div>

    <!-- Keywords table -->
    <table style="width:100%;border-collapse:collapse">
      <thead>
        <tr style="background:#f8fafc;border-bottom:2px solid #e2e8f0">
          <th style="padding:9px 14px;text-align:left;font-size:10px;color:#94a3b8;
                     text-transform:uppercase;letter-spacing:.07em;font-weight:700">#</th>
          <th style="padding:9px 14px;text-align:left;font-size:10px;color:#94a3b8;
                     text-transform:uppercase;letter-spacing:.07em;font-weight:700">Keyword</th>
          <th style="padding:9px 14px;text-align:center;font-size:10px;color:#94a3b8;
                     text-transform:uppercase;letter-spacing:.07em;font-weight:700">
                     Google Rank</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
  </div>"""


def build_email(data):
    checked  = data.get("last_updated_ist", "Today")
    date_str = (datetime.now(timezone.utc) + IST).strftime("%d %b %Y")
    brands   = "".join(brand_block(n, d) for n, d in data.get("brands", {}).items())

    return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/></head>
<body style="margin:0;padding:0;background:#f0f4f8;font-family:'Segoe UI',Arial,sans-serif">
<div style="max-width:700px;margin:0 auto;padding:20px 12px">

  <!-- Header -->
  <div style="background:linear-gradient(135deg,#1e3a8a 0%,#2563eb 100%);
              border-radius:16px;padding:30px 36px;margin-bottom:20px">
    <div style="font-size:28px;margin-bottom:8px">📈</div>
    <h1 style="margin:0;color:#fff;font-size:22px;font-weight:800">
      Daily SEO Rankings Report</h1>
    <p style="margin:6px 0 0;color:rgba(255,255,255,.75);font-size:13px">
      {date_str} &nbsp;·&nbsp; Data checked: {checked}
    </p>
  </div>

  <!-- Legend -->
  <div style="background:#fff;border:1px solid #e2e8f0;border-radius:10px;
              padding:12px 20px;margin-bottom:20px;font-size:12px;color:#64748b">
    <span style="background:#dcfce7;color:#15803d;padding:2px 8px;
                 border-radius:5px;font-weight:700;margin-right:4px">#1–3</span> Excellent &nbsp;&nbsp;
    <span style="background:#fef9c3;color:#a16207;padding:2px 8px;
                 border-radius:5px;font-weight:700;margin-right:4px">#4–10</span> Good (Page 1) &nbsp;&nbsp;
    <span style="background:#fee2e2;color:#dc2626;padding:2px 8px;
                 border-radius:5px;font-weight:700;margin-right:4px">Not Top 10</span> Needs work &nbsp;&nbsp;
    <span style="color:#cbd5e1;font-weight:700">—</span> No data yet
  </div>

  <!-- Brand sections -->
  {brands}

  <!-- Footer -->
  <div style="text-align:center;padding:16px 0;font-size:11px;color:#94a3b8">
    Auto-generated daily at 9 AM IST &nbsp;·&nbsp; Rankings checked at 2 AM IST<br>
    Bodyzone · Spa Kora · BIPS &nbsp;·&nbsp; India Google Rankings
  </div>

</div>
</body>
</html>"""


def main():
    print("Sending SEO Daily Email Report...")

    if not PASSWORD:
        print("ERROR: GMAIL_PASSWORD secret not set!"); sys.exit(1)

    try:
        with open("rankings.json", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"ERROR reading rankings.json: {e}"); sys.exit(1)

    date_str = (datetime.now(timezone.utc) + IST).strftime("%d %b %Y")
    subject  = f"📈 SEO Rankings Report — {date_str} | Bodyzone · Spa Kora · BIPS"
    html     = build_email(data)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"SEO Rankings <{SENDER}>"
    msg["To"]      = RECIPIENT
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.starttls()
        s.login(SENDER, PASSWORD)
        s.sendmail(SENDER, RECIPIENT, msg.as_string())

    print(f"Email sent successfully to {RECIPIENT}")


if __name__ == "__main__":
    main()
