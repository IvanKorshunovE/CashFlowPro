from rest_framework import routers

from revenue.views import RevenueStatisticByDateAndNameView

router = routers.DefaultRouter()
router.register("revenues", RevenueStatisticByDateAndNameView)

urlpatterns = router.urls

app_name = "revenue"
