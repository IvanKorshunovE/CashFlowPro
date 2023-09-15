from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from revenue.models import RevenueStatistic
from revenue.serializers import RevenueStatisticSerializer
from django.db.models import Sum


class RevenueStatisticByDateAndNameView(ListModelMixin, GenericViewSet):
    queryset = RevenueStatistic.objects.all()
    serializer_class = RevenueStatisticSerializer

    def get_queryset(self):
        queryset = self.queryset.select_related(
            "spend"
        ).values("date", "name").annotate(
            total_revenue=Sum("revenue"),
            total_spend=Sum("spend__spend"),
            total_impressions=Sum("spend__impressions"),
            total_clicks=Sum("spend__clicks"),
            total_conversion=Sum("spend__conversion"),
        )
        return queryset
