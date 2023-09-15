from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/revenue/", include("revenue.urls", namespace="revenues")),
    path("__debug__/", include("debug_toolbar.urls")),
]
