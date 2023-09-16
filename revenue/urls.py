from django.urls import path
from revenue import views

urlpatterns = [
    path(
        "revenue-statistics/",
        views.RevenueStatisticByDateAndNameView.as_view(),
        name="revenue-statistics"
    ),
]

app_name = "revenue"
