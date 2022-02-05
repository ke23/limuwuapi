
from django.urls import path
from . import views



urlpatterns = [
       path('memberships/<lohe>', views.MembershipView.as_view(), name='select'),
]