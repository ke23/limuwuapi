from fastapi import (
  FastAPI, Query, 
  HTTPException, File, 
  Form, UploadFile,
  BackgroundTasks
)
from fastapi.responses import (UJSONResponse,
    HTMLResponse,
    ORJSONResponse,
    StreamingResponse,
    FileResponse
)

from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from starlette.responses import RedirectResponse
from pydantic import BaseModel

from typing import Union, List, Dict, Any, Optional
from content import (
  Nekopoi, NekoResponseHome, NekoResponseDetail,
  Cinema, CinemaResponseMovies, CinemaResponseDetail,
  VirusTot, Pixiv, Const, Tiktok,
  ApkPure, ApkResponses, ApkDetailResponse,
  downloadBook, searchBook)
import io, subprocess, os,time, sys, random

desc = """
A collective list of free APIs for use in software and web development.

feedback? find me on Line: <a href=/line> @Al! </a>
"""
app = FastAPI(title="Zembut API", version="0.2.5", description=desc)
#app.mount("/static", StaticFiles(directory="data"), name="static")

if not os.path.exists(os.getcwd()+"/"+"data"):
  os.mkdir("data")

neko = Nekopoi()
cin = Cinema()
vir = VirusTot()
apk = ApkPure()
pix = Pixiv()
tik = Tiktok()

def counter(em, sec):
  if (sec < Const.ADAY and sec != 3):
    sec = Const.ADAY
  
  if sec > Const.WEEK3:
    sec = Const.WEEK3
    
  time.sleep(sec)
  
  if os.path.exists(em):
    os.remove(em)
  
@app.api_route("/", include_in_schema=False)
async def index():
  con = """Go to <a href='/docs'> /docs </a> for see documentation
  """
  return HTMLResponse(content=con)
  
@app.get("/line", include_in_schema=False)
async def line():
  return RedirectResponse("https://line.me/ti/p/~www.nekopoi.care")
  
@app.get("/api/nekopoi/", response_model=NekoResponseHome)
async def nekopoi_home_page(page: Union[str, int]):
  n = await neko.head(page)
  jsonable = jsonable_encoder(n)
  return ORJSONResponse(content=jsonable)
  
@app.get("/api/nekopoi/detail",
        description="Returning detail from url, Note: key is Dynamic",
        response_model=NekoResponseDetail)
async def nekopoi_detail_from_url(url: str = None,
      page: Union[str, int] = None,
      num: int = None):
  
  if (page and num):
    urll = (await neko.head(page))
    url = urll["host"]+urll["results"][int(num)-1]["url"]
  
  n = await neko.detail(url)
  jsonable = jsonable_encoder(n)
  return ORJSONResponse(content=jsonable)

@app.get("/api/cinema/list-country")
async def list_country():
  return cin.get_country
  
@app.get("/api/cinema/movies", response_model=CinemaResponseMovies)
async def cinema_movies(page: Union[str, int]):
  jsonable = jsonable_encoder(await cin.movies(page))
  return ORJSONResponse(content=jsonable)

@app.get("/api/cinema/country", response_model=CinemaResponseMovies)
async def cinema_country(country: str):
  jsonable = jsonable_encoder(await cin.from_country(country))
  return ORJSONResponse(jsonable)
  
@app.get("/api/cinema/drakor", response_model=CinemaResponseMovies)
async def cinema_drakor(page: Union[str, int]):
  jsonable = jsonable_encoder(await cin.drakor(page))
  return ORJSONResponse(content=jsonable)
  
@app.get("/api/cinema/western", response_model=CinemaResponseMovies)
async def cinema_western(page: Union[str, int]):
  jsonable = jsonable_encoder(await cin.western(page))
  return ORJSONResponse(content=jsonable)

@app.get("/api/cinema/detail", response_model=CinemaResponseDetail)
async def detail_cinema(uri: str):
  ja = await cin.detail(uri)
  jsonable = jsonable_encoder(ja)
  return ORJSONResponse(jsonable)
  
@app.post("/api/virtot/url-scan", name="Virtot Url Scan")
async def url_scan(url: str):
  s = await vir.url_scan(url)
  jsonable = jsonable_encoder(s)
  return ORJSONResponse(jsonable)

@app.post("/api/virtot/url-scan-report",
        name="Virtot Url Scan Report",
        description="You may also specify a scan_id (sha256-timestamp as returned by the URL submission API) to access a specific report.")
async def url_scan_report(resource: str):
  s = await vir.url_scan_report(resource)
  jsonable = jsonable_encoder(s)
  return ORJSONResponse(jsonable)

@app.get("/api/virtot/ip-report", name="Virtot Ip Report")
async def ip_report(ip: str):
  s = await vir.ip_report(ip)
  jsonable = jsonable_encoder(s)
  return ORJSONResponse(jsonable)
  
@app.get("/api/virtot/domain-repot", name="Virtot Domain Report")
async def domain_report(domain: str):
  s = await vir.domain_report(domain)
  jsonable = jsonable_encoder(s)
  return ORJSONResponse(jsonable)
  
@app.post("/api/virtot/file-scan", name="Virtot File Scan")
async def file_scan(file: UploadFile = File(...)):
  r = {"file": ("myfile", io.BytesIO(file.file.read()))}
  s = await vir.file_scan(r)
  jsonable = jsonable_encoder(s)
  return ORJSONResponse(jsonable)
  
@app.get("/api/virtot/file-report",
        name="Virtot File Scan Report",
        description="The resource argument can be the MD5, SHA-1 or SHA-256 of a file")
async def file_report(resource: str):
  s = await vir.file_report(resource)
  jsonable = jsonable_encoder(s)
  return ORJSONResponse(jsonable)
  
@app.get("/api/apk/search", response_model=ApkResponses)
async def search_apk(query: str = "pubg"):
  s = await apk.search_apk(query)
  jsonable = jsonable_encoder(s)
  return ORJSONResponse(jsonable)
  
@app.get("/api/apk/tranding", response_model=ApkResponses)
async def apk_tranding(page: Union[str, int] = 1):
  s = await apk.get_trending(page)
  jsonable = jsonable_encoder(s)
  return ORJSONResponse(jsonable)
  
@app.get("/api/apk/detail", response_model=ApkDetailResponse)
async def detail_apk(url: str):
  s = await apk.get_detail(url)
  jsonable = jsonable_encoder(s)
  return ORJSONResponse(jsonable)
  
@app.post("/api/mp4convert", description="simple convert Video(MP4) to any Audio format")
async def Mp4_Converter(format: str = Query("mp3", description="output format as (mp3, ogg, avi, etc.)", max_length=3),
          bitrate: str = Query("128k", description="audio bitrate for converted"),
          volume: str = Query("3", description="audio volume default 3(normal | recomended)"),
          codecs: str = Query("libmp3lame", description="codecs for audio default libmp3lame, see ffmpeg codecs for detail"),
          title: str = Query(..., description="title for your output file"),
          file: UploadFile = File(...)):
  name = file.filename if not " " in file.filename else file.filename.replace(" ", "_")
  name = Const.id_generator(random.randint(1, 7)) + "-" + name
  tmp =  open(f"data/{name}", "wb")
  tmp.write(await file.read())
  
  cmd = f"ffmpeg -y -i data/{name} -b:a {bitrate} -preset superfast -af volume={volume} -c:a libmp3lame -acodec {codecs} data/{title}.{format}" 
  call = subprocess.call(cmd, shell=True)
  
  if not call:
    os.remove(f"data/{name}")
    return {"status": True, "result":f"http://zembut.herokuapp.com/static/{title}.{format}"}
  os.remove(f"data/{name}")
  return {"status": False, "result": "unknown error, please try again"}
  
@app.api_route("/static/{name}", name="Mp3 Result")
async def x0__(name: str, bg: BackgroundTasks,
        keep: Optional[Union[str, int]] = Query(None)):
  """
  - **name**: specific name of file include extension, ex: myfile.mp3
  - **keep**: specification of time in seconds for file deletion, default is 3 seconds, max 1814000 seconds or 3 weeks
  """
  if not os.path.exists(os.getcwd()+f"/data/{name}"):
    return {"status": False, "msg": "file doesn't exists"}
  
  if keep:
    bg.add_task(counter, os.getcwd()+f"/data/{name}", sec=int(keep))
  else:
    bg.add_task(counter, os.getcwd()+f"/data/{name}", sec=3)
  
  return FileResponse(f"data/{name}")
  
@app.get("/api/illust/search", name="Search Illust")
async def search_illust(q: str):
  jsonable = jsonable_encoder(await pix._search(q))
  return ORJSONResponse(jsonable)

@app.get("/api/illust/random")
async def random_illust():
  jsonable = jsonable_encoder(await pix.random())
  return ORJSONResponse(jsonable)
  
@app.get("/api/tiktok/stream")
async def tiktok_video(url: str):
  urrl = await tik.get_video_url(url)
  jsonable = jsonable_encoder(urrl)
  return ORJSONResponse(jsonable)
  
@app.get("/api/tiktok/user-post", include_in_schema=False)
async def tiktok_user_post(user_id: str, secUid: str):
  data = await tik.userPosts(user_id, secUid)
  jsonable = jsonable_encoder(data)
  return ORJSONResponse(jsonable)

@app.get("/api/anybook/search")
async def search_books(q: str):
  data = await searchBook(q)
  jsonable = jsonable_encoder(data)
  return ORJSONResponse(jsonable)
  
@app.get("/api/anybook/download")
async def download_book(url: str):
  data = await downloadBook(url)
  jsonable = jsonable_encoder(data)
  return ORJSONResponse(jsonable)