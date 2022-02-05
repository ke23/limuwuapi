
import uuid

from ninja import Router
from ninja.security import APIKeyQuery

from django.db.models import F
from asgiref.sync import sync_to_async

from .schemas import Schema400, Schema401, SchemaApkSearch
from .generators import check_apikey, check_apikey_free
from .models import FreeAPIKey, PremiumAPIKey

from core.listapi.apkpure.apk_sync import ApkPure
from core.listapi.books import books


class InvalidToken(Exception):
    pass


class QueryAPIKeyAuth(APIKeyQuery):
    param_name = "apikey"

    def authenticate(self, request, key: str):
        if key is None:
            return False
        else:
            try:
                if uuid.UUID(str(key)): # Validate FreeAPIKey with uuid
                    check = check_apikey_free(key)
                    if check:
                        api_key = check.api_key
                        user = check.user    # sewaktu2 butuh
                        return api_key
            except (ValueError, IndexError, TypeError):
                check = check_apikey(key) # Validate PremiumAPIKey
                if check: 
                    api_key = check.api_key
                    user = check.user    # sewaktu2 butuh
                    return api_key
                else:
                    print('else hereeeeee')
                    return False


router = Router()
auth = QueryAPIKeyAuth()

# =======================================================================
# async def free_apikey_qs():
#     return await sync_to_async(list)(FreeAPIKey.objects.all())

# async def premium_apikey_qs():
#     return await sync_to_async(list)(PremiumAPIKey.objects.all())
# =======================================================================

FREE_APIKEY_QUERYSET = FreeAPIKey.objects.all()
PREMIUM_APIKEY_QUERYSET = PremiumAPIKey.objects.all()


apk = ApkPure()

# def increment_request_total(apikey: str):
#     if apikey in FREE_APIKEY_QUERYSET:
#         apikey.freeapikeycounter.update(req_tot=F('req_tot') + 1)
#     elif apikey in PREMIUM_APIKEY_QUERYSET:
#         apikey.premiumapikeycounter.update(req_tot=F('req_tot') + 1)
#     return


@router.get("/apk/search", auth=auth, response={200: SchemaApkSearch, 400: Schema400, 401: Schema401}) #auth=auth sudah memvalidasi apakah APIkeynya valid atau tidak
def search_apk(request, q: str):
    if request.auth in FREE_APIKEY_QUERYSET:
        if request.auth.freeapikeycounter.is_max:
            return 400, {'message': 'Maximum Limit Request Reached !'}
        else:
            src = apk.search_apk(q)
            request.auth.freeapikeycounter.req_tot = F('req_tot') + 1 # apikey.freeapikeycounter.update(req_tot=F('req_tot') + 1)
            request.auth.freeapikeycounter.save()
            return 200, src
            
    if request.auth in PREMIUM_APIKEY_QUERYSET:
        if request.auth.premiumapikeycounter.is_max:
            return 400, {'message': 'Maximum Limit Request Reached !'}
        else:
            print('this is from hereeeeeeeeeeeeeee')
            src = apk.search_apk(q)
            print('dibawahnya ini HASIL SRC')
            print(src)
            request.auth.premiumapikeycounter.req_tot = F('req_tot') + 1
            request.auth.premiumapikeycounter.save()
            return 200, src
    
    else: # Bagian else ini sptnya tidak akan tereksekusi krn APIKEY sudah di validasi di authenticate()
        print('gk ada dimana2')
        return 400, {'error': 'NOT AN API KEY'}
    
    

# @router.get("/apk/search", auth=auth, response={200: SchemaApkSearch, 400: Schema400, 401: Schema401}) #auth=auth sudah memvalidasi apakah
# def search_apk(request, q: str):
#     increment_request_total(request.auth)
#     src = apk.search_apk(q)
#     return 200, src