from pydantic import BaseModel
from typing import Union, List, Dict, Any


# class ApkResponses(BaseModel):
#   results: List[Dict[Union[str], Any]]
  
  # class Config:
  #   scheme_extra = {
  #     "example": {
  #       "results": [{
  #         "title": "PUBG Mobile",
  #         "url": "https://apkpure.com/pubg-mobile-4-android-i/com.tencent.ig",
  #         "img": "https://image.winudf.com/v2/image1/Y29tLnRlbmNlbnQuaWdfaWNvbl8xNTc2MDIxMjgwXzA4MA/icon.png?w=100&fakeurl=1",
  #         "rating": "average: 9.1 out of 10"
  #       },{
  #         "title": "Mobile Legeng: Bang Bang",
  #         "url": "https://m.apkpure.com/mobile-legends-bang-bang/com.mobile.legends",
  #         "img": "https://image.winudf.com/v2/image1/Y29tLm1vYmlsZS5sZWdlbmRzX2ljb25fMTU3NDEzNDM0MF8wNTU/icon.png?w=100&fakeurl=1",
  #         "rating": "average: 9.1 out of 10"
  #       }]
  #     }
  #   }
    
    
class ApkDetailResponse(BaseModel):
  title: str = "PUBG Mobile"
  icon: str
  version: str = "1.69.69"
  avg: str = "average: 9.1 out of 10"
  desc: str
  download_url: str
  size: str = "500MB"
  
  class Config:
    scheme_extra = {
      "example": {
        "title": "PUBG Mobile",
        "icon": "https://image.winudf.com/v2/image1/Y29tLnRlbmNlbnQuaWdfaWNvbl8xNTc2MDIxMjgwXzA4MA/icon.png?w=100&fakeurl=1",
        "version": "1.69.69",
        "avg": "average: 9.1 out of 10",
        "desc": "The official PLAYERUNKNOWN'S BATTLEGROUNDS designed exclusively for mobile. Play fr...",
        "download_url": "https://download.apkpure.com/b/APK/Y29tLn4MD...VCRyBNT0JJTEV...MTcuMF9hcGtwdXJlLmNvbS5hcGs&as=...&ai=886278234&2Cat&k=....&_p=Y29tLnR....&w=3",
        "size": "500MB"
      }
    }