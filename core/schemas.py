
from typing import Union, List, Dict, Any
from ninja import Schema

class Schema400(Schema):
    message: str

class Schema401(Schema):
    detail: str

class SchemaApkSearch(Schema):
  results: List[Dict[Union[str], Any]]