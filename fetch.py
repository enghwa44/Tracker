import urllib.request, json, re, urllib.parse
from datetime import datetime

headers_json = {
  "User-Agent": "Mozilla/5.0 Chrome/120.0.0.0 Safari/537.36",
  "Accept": "application/json",
  "Referer": "https://m.stock.naver.com/",
}

headers_krx = {
  "User-Agent": "Mozilla/5.0 Chrome/120.0.0.0 Safari/537.36",
  "Accept": "application/json, text/plain, */*",
  "Referer": "https://www.krx.co.kr/",
  "Origin": "https://www.krx.co.kr",
}

def get_json(url, headers=None):
  try:
    req = urllib.request.Request(url, headers=headers or headers_json)
    with urllib.request.urlopen(req, timeout=10) as r:
      return json.loads(r.read().decode("utf-8"))
  except Exception as e:
    print("fail", url, str(e)[:80])
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

# V-KOSPI200 - KRX 공식 API
today = datetime.utcnow().strftime("%Y%m%d")
krx_url = f"https://data-dbg.krx.co.kr/svc/apis/idx/volat_idx/getVoltIdxDd?basDd={today}&idxNm=VKOSPI200&apiKey=test"
d3 = get_json(krx_url, headers_krx)
if d3:
  print("KRX response:", str(d3)[:200])

# 대안: KRX 정식 데이터포털
if not vkospi:
  # 네이버 금융 VKOSPI 직접 데이터 (iframe 소스)
  try:
    req = urllib.request.Request(
      "https://finance.naver.com/sise/sise_index_day.naver?code=KOSPI_VIX&page=1",
      headers={**headers_json, "Accept": "text/html", "Accept-Language": "ko-KR"}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
      txt = r.read().decode("euc-kr", errors="ignore")
      # 테이블에서 첫 번째 소수 2자리 숫자 (10~100 범위)
      nums = re.findall(r'<td[^>]*>\s*(\d{2,3}\.\d{2})\s*</td>', txt)
      print("VIX table nums:", nums[:10])
      for n in nums:
        v = float(n)
        if 10 < v < 150:
          vkospi = v
          print("VKOSPI (table):", vkospi)
          break
  except Exception as e:
    print("VIX table fail:", str(e)[:80])

print("VKOSPI final:", vkospi)
result = json.dumps({"price":price,"kospi200":kospi200,"vkospi":vkospi,"updated":datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")})
print("result:", result)
open("price.json","w").write(result)
