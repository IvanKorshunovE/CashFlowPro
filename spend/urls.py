from django.urls import path
from spend import views

urlpatterns = [
    path(
        "spend-statistics/",
        views.SpendStatisticByDateAndNameView.as_view(),
        name="spend-statistics"
    ),
]

app_name = "spending"
