from rest_framework import generics

from django.db.models import Sum

from revenue.models import RevenueStatistic
from revenue.serializers import RevenueStatisticSerializer


class RevenueStatisticByDateAndNameView(generics.ListAPIView):
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
