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

def get_html(url):
  try:
    req = urllib.request.Request(url, headers=headers_html)
    with urllib.request.urlopen(req, timeout=10) as r:
      return r.read().decode("euc-kr", errors="ignore")
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

# V-KOSPI200 - 현재값(now) 영역에서만 파싱, 범위 10~150
txt = get_html("https://finance.naver.com/sise/sise_index.naver?code=KOSPI_VIX")
if txt:
  # now 영역 추출 후 첫 번째 소수점 숫자
  now_section = re.search(r'now[^<]{0,200}?([\d]{2,3}\.\d{2})', txt)
  if now_section:
    try:
      v = float(now_section.group(1))
      if 5 < v < 150:
        vkospi = v
        print("VKOSPI (now section):", vkospi)
    except: pass

  if not vkospi:
    # _nowVal 패턴
    m = re.search(r'_nowVal[^>]*>([\d]{2,3}\.\d{2})', txt)
    if m:
      try:
        v = float(m.group(1))
        if 5 < v < 150:
          vkospi = v
          print("VKOSPI (_nowVal):", vkospi)
      except: pass

  if not vkospi:
    # 전체에서 10~99 범위 소수 첫 번째
    matches = re.findall(r'\b([1-9]\d\.\d{2})\b', txt[:5000])
    for mv in matches:
      try:
        v = float(mv)
        if 10 < v < 100:
          vkospi = v
          print("VKOSPI (range match):", vkospi)
          break
      except: pass

print("VKOSPI final:", vkospi)

result = json.dumps({"price":price,"kospi200":kospi200,"vkospi":vkospi,"updated":datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")})
print("result:", result)
open("price.json","w").write(result)
