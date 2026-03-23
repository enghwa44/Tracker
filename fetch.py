import urllib.request, json
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

d = get("https://m.stock.naver.com/api/stock/498400/basic")
if d:
  try: price = int(str(d.get("closePrice","0")).replace(",",""))
  except: pass
print("KODEX:", price)

d2 = get("https://m.stock.naver.com/api/index/KOSPI200/basic")
if d2:
  try: kospi200 = float(str(d2.get("closePrice","0")).replace(",",""))
  except: pass
print("KOSPI200:", kospi200)

for code in ["VKOSPI", "KOSPI VIX"]:
  import urllib.parse
  d3 = get("https://m.stock.naver.com/api/index/" + urllib.parse.quote(code) + "/basic")
  if d3:
    try:
      vkospi = float(str(d3.get("closePrice","0")).replace(",",""))
      print("VKOSPI:", vkospi)
      break
    except: pass

result = json.dumps({"price":price,"kospi200":kospi200,"vkospi":vkospi,"updated":datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")})
print("result:", result)
open("price.json","w").write(result)
