from rest_framework import routers

from revenue.views import RevenueStatisticByDateAndNameView

router = routers.DefaultRouter()
router.register("statistics", RevenueStatisticByDateAndNameView)

urlpatterns = router.urls

app_name = "statistics"
