
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# from limuwuapi.core.default_schema import counter


User = get_user_model()

# CUSTOM MIXIN UPDATE FOR NON QUERYSET 
class UpdateMixin(object):
    def update(self, **kwargs):
        if self._state.adding:
            raise self.DoesNotExist
        for field, value in kwargs.items():
            setattr(self, field, value)
        self.save(update_fields=kwargs.keys())

# Validators
def freeapikey_max_request(value):
    if value == 5:
        raise ValidationError(
            _('%(value)s Total max request tercapai!'),
            params={'value': value},
        )



class PremiumAPIKey(models.Model):
    prefix      = models.CharField(max_length=8, primary_key=True)
    hashed_key  = models.CharField(max_length=100)
    user        = models.ForeignKey(User, related_name='prem_key', on_delete=models.CASCADE)
    label       = models.CharField(max_length=40)
    revoked     = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    expires_at  = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering            = ["-created_at"]
        verbose_name        = "Premium API key"
        verbose_name_plural = "Premium API keys"

    @property
    def is_valid(self):
        if self.revoked:
            return False

        if not self.expires_at:
            return True  # No expiration

        return self.expires_at >= timezone.now()

    def __str__(self):
        return f"{self.user.username}<{self.prefix}>"



class FreeAPIKey(models.Model):
    key         = models.UUIDField(primary_key=True, editable=False)
    user        = models.ForeignKey(User, related_name='free_key', on_delete=models.CASCADE)
    label       = models.CharField(max_length=40)
    revoked     = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    expires_at  = models.DateTimeField(null=True, blank=True)


    class Meta:
        ordering            = ["-created_at"]
        verbose_name        = "Free API key"
        verbose_name_plural = "Free API keys"

    @property
    def is_valid(self):
        if self.revoked:
            return False

        if not self.expires_at:
            return True  # No expiration

        return self.expires_at >= timezone.now()

    def __str__(self):
        return f"{self.user.username} - Free ApiKey: <{self.key}>"


class FreeAPIKeyCounter(UpdateMixin, models.Model):
    free_key    = models.OneToOneField(FreeAPIKey, on_delete=models.CASCADE)
    req_tot     = models.IntegerField(default=0, editable=False, validators=[freeapikey_max_request])

    @property
    def is_max(self):
        if self.req_tot >= 15:
            return True
        return False

    def __str__(self):
        return f"Total Free Request dari user {self.free_key.user.username} : {self.req_tot}"

class PremiumAPIKeyCounter(UpdateMixin, models.Model):
    premium_key = models.OneToOneField(PremiumAPIKey, on_delete=models.CASCADE)
    req_tot     = models.IntegerField(default=0, editable=False)

    @property
    def is_max(self):
        print("NGITUUUNNG")
        if self.req_tot >= 50:
            return True
        print("BAWAHNYA NGITUUNG")
        return False

    def __str__(self):
        return f"Total Premium Request dari user {self.premium_key.user.username} : {self.req_tot}"