import httpx, re
from bs4 import BeautifulSoup
from collections import defaultdict

search_url = "https://b-ok.asia/s/{}"
host = "https://b-ok.asia"

def _request(url):
  with httpx.Client(http2=True) as req:
    res = req.get(url)
    if res.status_code != 200:
      return False
    return res
    
def downloadBook(url):
  
  res = _request(url)
  if not res:
    return {"status":False, "msg": "Unknown error, check your url"}
    
  r = r"bookProperty property_isbn\s(\d+)"
  result = defaultdict()
  soup = BeautifulSoup(res.content, "lxml")
  body = soup.find("div", class_="col-sm-9")
  try:
    udl = host + soup.find("a", class_="btn btn-primary dlButton addDownloadedBook")["href"]
  except TypeError:
    udl = None
  
  try:
    cat = body.find("div", class_="bookProperty property_categories").find("div", class_="property_value").text
  except AttributeError:
    cat = "Unknown"
  result["title"] = body.h1.text.strip()
  result["page"] = body.find("div", class_="bookProperty property_pages").find("div",class_= "property_value").text
  result["desc"] = body.find("div", id="bookDescriptionBox").text.strip()
  result["category"] = cat
  result["isbn"] = [i.text.strip() for i in body.find_all("div", class_=re.findall(r, str(body)))]
  result["download"] = udl if udl is not None else "None"
  return result
    
def searchBook(q):
  results = {"results":[]}
  req = _request(search_url.format(q))
  if req:
    soup = BeautifulSoup(req.content, "lxml")
    for i in soup.find_all("table", class_="resItemTable"):
      try:
        year = i.find("div", class_="bookProperty property_year").find("div", class_="property_value").text
      except AttributeError:
        year = "Unknown"
        
      lang = i.find("div", class_="bookProperty property_language").find("div", class_="property_value").text
      file = i.find("div", class_="bookProperty property__file").find("div", class_="property_value").text
      results["results"].append({
        "title": i.h3.text.strip(),
        "url": host + i.h3.a.get("href"),
        "img": i.find("img").get("data-src"),
        "year": year,
        "lang": lang,
        "size": file
      })
    return results
  
  return {"status": False, "msg": "can't found any books your search"}