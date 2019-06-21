from django.urls import path,include
from . import views

urlpatterns = [
    path("login", views.log_in),
    path("register", views.register),
    path("logout",views.log_out),
    path("image",views.parse_image),
    path("statistics",views.get_statistics),
    path("foodList",views.get_foodlist),
    path("test",views.test),
    path("daily",views.save_daily_record),
]
