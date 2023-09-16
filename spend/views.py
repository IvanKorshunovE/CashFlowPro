from drf_spectacular.utils import extend_schema
from rest_framework import generics

from revenue.models import RevenueStatistic
from spend.models import SpendStatistic
from spend.serializers import SpendStatisticSerializer
from django.db.models import Sum, Subquery, OuterRef, DecimalField


class SpendStatisticByDateAndNameView(generics.ListAPIView):
    serializer_class = SpendStatisticSerializer

    def get_queryset(self):
        total_revenue_subquery = RevenueStatistic.objects.filter(
            spend=OuterRef("pk")
        ).values("spend").annotate(
            total_revenue=Sum("revenue")
        ).values("total_revenue")[:1]

        queryset = SpendStatistic.objects.values("date", "name").annotate(
            total_spend=Sum("spend"),
            total_impressions=Sum("impressions"),
            total_clicks=Sum("clicks"),
            total_conversion=Sum("conversion"),
            total_revenue=Sum(
                Subquery(total_revenue_subquery), output_field=DecimalField()
            ),
        )

        return queryset

    @extend_schema(
        description="Retrieve a list of spend statistics by date and name with aggregated data."
    )
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
