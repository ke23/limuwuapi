
import uuid
from django.contrib import admin, messages

from .models import PremiumAPIKey, FreeAPIKey, PremiumAPIKeyCounter, FreeAPIKeyCounter
from .generators import generate_key


@admin.action(description="Revoke selected API keys")
def revoke_key(modeladmin, request, queryset):
    queryset.update(revoked=True)


@admin.register(PremiumAPIKey)
class PremiumAPIKeyAdmin(admin.ModelAdmin):
    list_display = [
        "prefix",
        "user",
        "label",
        "created_at",
        "expires_at",
        "revoked",
        "is_active",
    ]
    readonly_fields = ["prefix", "hashed_key", "created_at"]
    actions = [revoke_key]
    list_filter = ["revoked"]

    @admin.display
    def is_active(self, obj: PremiumAPIKey):
        return obj.is_valid

    is_active.boolean = True  # Display property as boolean

    def save_model(self, request, obj: PremiumAPIKey, form, change):
        if not obj.prefix:  # New API key
            key = generate_key()
            obj.prefix = key.prefix
            obj.hashed_key = key.hashed_key

            if request:
                messages.add_message(
                    request,
                    messages.WARNING,
                    f"The API key for {obj} is '{key.prefix}-{key.key}'."
                    "You should store it somewhere safe: "
                    "you will not be able to see the key again.",
                )
        obj.save()

        return obj


@admin.register(FreeAPIKey)
class FreeAPIKeyAdmin(admin.ModelAdmin):
    list_display = [
        "key",
        "user",
        "label",
        "created_at",
        "expires_at",
        "revoked",
        "is_active",
    ]
    readonly_fields = ["key", "created_at"]
    actions = [revoke_key]
    list_filter = ["revoked"]

    @admin.display
    def is_active(self, obj: FreeAPIKey):
        return obj.is_valid

    is_active.boolean = True  # Display property as boolean

    def save_model(self, request, obj: FreeAPIKey, form, change):
        if not obj.key:  # New API key
            obj.key = str(uuid.uuid4())

            if request:
                messages.add_message(request,messages.WARNING, f"The API key for {obj} is '{obj.key}'.")

        obj.save()
        return 

admin.site.register(FreeAPIKeyCounter)
admin.site.register(PremiumAPIKeyCounter)
# @admin.register(FreeAPIKeyCounter)
# class FreeAPIKeyCounterAdmin(admin.ModelAdmin):
#     list_display = [
#         "key",
#         "req_tot",
#     ]
#     readonly_fields = ["key"]
#     # actions = [revoke_key]
#     # list_filter = ["revoked"]

#     @admin.display
#     def is_active(self, obj: FreeAPIKey):
#         return obj.is_valid

#     is_active.boolean = True  # Display property as boolean

#     def save_model(self, request, obj: FreeAPIKey, form, change):
#         if not obj.key:  # New API key
#             obj.key = str(uuid.uuid4())

#             if request:
#                 messages.add_message(request,messages.WARNING, f"The API key for {obj} is '{obj.key}'.")

#         obj.save()
#         return 