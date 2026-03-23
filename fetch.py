import urllib.request, json, urllib.parse
from datetime import datetime

headers = {
  "User-Agent": "Mozilla/5.0 Chrome/120.0.0.0 Safari/537.36",
  "Accept": "application/json",
  "Referer": "https://m.stock.naver.com/",
}

def get(url):
  try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as r:
      return json.loads(r.read().decode("utf-8"))
  except Exception as e:
    print("fail", url, e)
    return None

price, kospi200, vkospi = 0, 0.0, 0.0

# KODEX 현재가
d = get("https://m.stock.naver.com/api/stock/498400/basic")
if d:
  try: price = int(str(d.get("closePrice","0")).replace(",",""))
  except: pass
print("KODEX:", price)

# 코스피200 지수 - 여러 코드 시도
for code in ["KPI200", "KOSPI200", "KS200"]:
  d2 = get("https://m.stock.naver.com/api/index/" + code + "/basic")
  if d2 and d2.get("closePrice"):
    try:
      kospi200 = float(str(d2.get("closePrice","0")).replace(",",""))
      if kospi200 > 0:
        print("KOSPI200 (" + code + "):", kospi200)
        break
    except: pass

# V-KOSPI200 - 여러 코드 시도
for code in ["VKOSPI", "VIX", "KOSPI_VIX", "KOSPI%20VIX"]:
  d3 = get("https://m.stock.naver.com/api/index/" + code + "/basic")
  if d3 and d3.get("closePrice"):
    try:
      vkospi = float(str(d3.get("closePrice","0")).replace(",",""))
      if vkospi > 0:
        print("VKOSPI (" + code + "):", vkospi)
        break
    except: pass

result = json.dumps({"price":price,"kospi200":kospi200,"vkospi":vkospi,"updated":datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")})
print("result:", result)
open("price.json","w").write(result)
