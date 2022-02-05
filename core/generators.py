
from collections import namedtuple

from django.contrib.auth.hashers import check_password, make_password
from django.utils.crypto import get_random_string

from .models import PremiumAPIKey, FreeAPIKey, User




KeyData = namedtuple("KeyData", "prefix key hashed_key")

def generate_key() -> KeyData:
    prefix = get_random_string(8)
    key = get_random_string(56)
    hashed_key = make_password(key)
    return KeyData(prefix, key, hashed_key)




KeyAndUser = namedtuple("KeyAndUser", "api_key user")

def check_apikey(api_key: str) -> KeyAndUser:

    if not api_key: # ini buat ngecek, kalau parameter api_key gk ada valuenya, return False, jadi user gk input apikey isinya None
        return False

    if "-" not in api_key:  # Check API key format ({prefix} - {key})
        return False
    data = api_key.split("-")

    prefix = data[0]
    key = data[1]


    premium_key = PremiumAPIKey.objects.filter(prefix=prefix).first()

    if not premium_key:
        return False

    if not check_password(key, premium_key.hashed_key):
        return False

    if not premium_key.is_valid:
        return False

    user = premium_key.user

    if not user:
        return False

    if not user.is_active:
        return False

    return KeyAndUser(premium_key, user)
    # return premium_key #ini yang kereturn def __str__ nya yg di model premium key, krn ini instance / record dr model tsb


def check_apikey_free(api_key: str) -> KeyAndUser:

    if not api_key:
        return False
    
    free_key = FreeAPIKey.objects.filter(key=api_key).first() # apakah harus menggunakan try ?

    if not free_key:
        return False
    
    if not free_key.is_valid:
        return False

    user = free_key.user

    if not user:
        return False
    
    if not user.is_active:
        return False
    
    return KeyAndUser(free_key, user)
    # return free_key # ini yg kereturn def __str__ nya yg di model free key, krn ini instance / record dr model tsb

# class HeaderAPIKeyAuth(APIKeyHeader):
#     param_name = "X-API-Key"

#     def authenticate(self, request, key):
#         user = check_apikey(key)

#         if not user:
#             return False

#         request.user = user
#         return user

