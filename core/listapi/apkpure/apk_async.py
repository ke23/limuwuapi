import httpx
from bs4 import BeautifulSoup
from collections import defaultdict
from .agent import ua_random

class ApkPure:
  def __init__(self):
    self.host = "http://apkpure.com"
    self.search = self.host+"/search?q={}"
    self.trending = self.host+"/topic/trending-games?page={}"
    self.session = httpx.AsyncClient
    self.hd = {
      "User-Agent": ua_random,
      "Connection": "keep-alive",
      "Cache-Control": "no-cache",
    }
  
  def _valid(self, res):
    return True if res.status_code <= 200 else False

  async def _request(self, meth, url, *args, **kwgs):
    async with self.session(http2=True, headers=self.hd) as req:
      res = await req.request(meth, url, *args, **kwgs)
      return res if self._valid(res) else False
  
  async def get_dw_url(self, u):
    response = await self._request("GET", u)
    soup = BeautifulSoup(response.content, "lxml")
    page = soup.find("div", class_="main page-q")
    find_url = page.find("div", class_ = "fast-download-box fast-bottom")
    return find_url.find("a", class_="ga")["href"]
    
  async def search_apk(self, query: str):
    res = await self._request("GET", self.search.format(query))
    if not res:
      return {"status":False, "msg":"Unknown error"}
    
    result = defaultdict()
    result["results"] = []
    soup = BeautifulSoup(res.content, "lxml")
    ret = soup.find("div", attrs={"id":"search-res"})
    dl = ret.find_all("dl", class_="search-dl")
    for i in dl:
      att1 = i.a.attrs
      img = i.img.get("src")
      sc = i.find("span", class_="score")
      if not sc:
        ra = "average: 0.0 out of 10"
      else:
        ra = sc["title"]
      result["results"].append({
        "title":att1["title"],
        "url":self.host+att1["href"],
        "img":img,
        "rating":ra
      })
    return result
  
  async def get_detail(self, url: str):
    res = await self._request("GET", url)
    if not res:
      return {"status":False, "msg":"Unknown error"}
    
    r = defaultdict()
    soup = BeautifulSoup(res.content, "lxml")
    box = soup.find("div", class_ = "box")
    
    u = await self.get_dw_url(
            self.host+box.find("div", class_="ny-down")\
            .find("a", class_="da")["href"])
    r["title"] = box.h1.text.strip()
    r["icon"]  = box.find("div", class_="icon").img.get("src", None)
    r["version"] = box.find("div", class_="details-sdk").span.text.strip()
    r["avg"] = box.find("div", class_="stars")["title"]
    r["desc"] = box.find("div", class_="description").find("div", class_="content").text
    r["download_url"] = u
    r["size"] = box.find("span", class_="fsize").text.strip("()")
    return r
  
  async def get_trending(self, page=1):
    res = await self._request("GET", self.trending.format(page))
    if not res:
      return {"status":False, "msg":"Unknown error"}
    
    r = defaultdict()
    r["results"]  = []
    soup = BeautifulSoup(res.content, "lxml")
    box = soup.find_all("div", class_="box editors_m")
    for i in box:
      att = i.a.attrs
      img = i.img.get("src")
      ra = i.find("div", class_="topic-rating")
      if not ra:
        ret = "average: 0.0 out of 10"
      else:
        ret = ra["title"]
      
      r["results"].append({
        "title":att["title"],
        "url":self.host+att["href"],
        "img":img,
        "rating":ret
      })
    return r

