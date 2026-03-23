import urllib.request, json, re
from datetime import datetime

headers_json = {
  "User-Agent": "Mozilla/5.0 Chrome/120.0.0.0 Safari/537.36",
  "Accept": "application/json",
  "Referer": "https://m.stock.naver.com/",
}

headers_html = {
  "User-Agent": "Mozilla/5.0 Chrome/120.0.0.0 Safari/537.36",
  "Accept": "text/html",
  "Accept-Language": "ko-KR,ko;q=0.9",
}

def get_json(url):
  try:
    req = urllib.request.Request(url, headers=headers_json)
    with urllib.request.urlopen(req, timeout=10) as r:
      return json.loads(r.read().decode("utf-8"))
  except Exception as e:
    print("fail json", url, e)
    return None

def get_html(url, enc="euc-kr"):
  try:
    req = urllib.request.Request(url, headers=headers_html)
    with urllib.request.urlopen(req, timeout=10) as r:
      return r.read().decode(enc, errors="ignore")
  except Exception as e:
    print("fail html", url, e)
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

# V-KOSPI200 - HTML 디버그 출력
txt = get_html("https://finance.naver.com/sise/sise_index.naver?code=KOSPI_VIX")
if txt:
  # 처음 3000자 출력 (로그에서 패턴 확인용)
  print("=== VIX HTML SNIPPET ===")
  print(txt[:3000])
  print("=== END SNIPPET ===")
else:
  print("VIX HTML 가져오기 실패")

print("VKOSPI:", vkospi)
result = json.dumps({"price":price,"kospi200":kospi200,"vkospi":vkospi,"updated":datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")})
print("result:", result)
open("price.json","w").write(result)
