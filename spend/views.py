from rest_framework import generics

from revenue.models import RevenueStatistic
from spend.models import SpendStatistic
from spend.serializers import SpendStatisticSerializer
from django.db.models import Sum, Subquery, OuterRef


class SpendStatisticByDateAndNameView(generics.ListAPIView):
    serializer_class = SpendStatisticSerializer

    def get_queryset(self):
        queryset = SpendStatistic.objects.values("date", "name").annotate(
            total_spend=Sum("spend"),
            total_impressions=Sum("impressions"),
            total_clicks=Sum("clicks"),
            total_conversion=Sum("conversion"),
            total_revenue=Sum(
                Subquery(
                    RevenueStatistic.objects.filter(
                        spend=OuterRef("pk")
                    ).values("revenue").annotate(
                        revenue_sum=Sum("revenue")
                    ).values("revenue_sum")
                )
            ),
        )

        return queryset
