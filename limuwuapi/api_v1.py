
import orjson
from ninja import NinjaAPI
from ninja.renderers import BaseRenderer

from core.api import router

# RENDERER (based from docs)
class ORJSONRenderer(BaseRenderer):
    media_type = "application/json"

    def render(self, request, data, *, response_status):
        return orjson.dumps(data)

renderer = ORJSONRenderer()

# ==========================================
# Using Router (Sebenarnya tanpa router bisa, cuma siapa tau untuk keperluan kedepan butuh scaling)
api_v1 = NinjaAPI(version='1.0.0', renderer=renderer)
api_v1.add_router(prefix='', router=router)

