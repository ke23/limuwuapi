from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import check_password, make_password
from django.conf.global_settings import PASSWORD_HASHERS


prefix = get_random_string(8)
key = get_random_string(56)
hashed_key = make_password(key)

print(prefix)
print(key)
print(hashed_key)