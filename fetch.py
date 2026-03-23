import urllib.request, json, re
from datetime import datetime

headers_json = {
  "User-Agent": "Mozilla/5.0 Chrome/120.0.0.0 Safari/537.36",
  "Accept": "application/json",
  "Referer": "https://m.stock.naver.com/",
}

def get_json(url):
  try:
    req = urllib.request.Request(url, headers=headers_json)
    with urllib.request.urlopen(req, timeout=10) as r:
      return json.loads(r.read().decode("utf-8"))
  except Exception as e:
    print("fail", url, e)
    return None

price, kospi200, vkospi = 0, 0.0, 0.0

# KODEX 현재가
d = get_json("https://m.stock.naver.com/api/stock/498400/basic")
if d:
  try: price = int(str(d.get("closePrice","0")).replace(",",""))
  except: pass
print("KODEX:", price)

# 코스피200
d2 = get_json("https://m.stock.naver.com/api/index/KPI200/basic")
if d2:
  try: kospi200 = float(str(d2.get("closePrice","0")).replace(",",""))
  except: pass
print("KOSPI200:", kospi200)

# V-KOSPI200 - 네이버 홈 시세 데이터 (multiSise API)
d3 = get_json("https://m.stock.naver.com/api/stock/VKOSPI/basic")
if d3:
  try:
    vkospi = float(str(d3.get("closePrice","0")).replace(",",""))
    print("VKOSPI (stock api):", vkospi)
  except: pass

# 대안 1: 네이버 지수 검색 API
if not vkospi:
  d4 = get_json("https://m.stock.naver.com/api/index/VKOSPI200/basic")
  if d4:
    try:
      vkospi = float(str(d4.get("closePrice","0")).replace(",",""))
      print("VKOSPI (VKOSPI200):", vkospi)
    except: pass

# 대안 2: 네이버 금융 검색 결과
if not vkospi:
  headers_s = {**headers_json, "Accept": "application/json, text/plain"}
  try:
    req = urllib.request.Request(
      "https://ac.finance.naver.com/ac?q=VKOSPI&q_enc=UTF-8&t_koreng=1&st=111&r_lt=111",
      headers=headers_s
    )
    with urllib.request.urlopen(req, timeout=10) as r:
      txt = r.read().decode("utf-8", errors="ignore")
      print("search result:", txt[:200])
  except Exception as e:
    print("search fail:", e)

print("VKOSPI final:", vkospi)
result = json.dumps({"price":price,"kospi200":kospi200,"vkospi":vkospi,"updated":datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")})
print("result:", result)
open("price.json","w").write(result)
