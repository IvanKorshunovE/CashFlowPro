from rest_framework import generics
from spend.models import SpendStatistic
from spend.serializers import SpendStatisticSerializer
from django.db.models import Sum


class SpendStatisticByDateAndNameView(generics.ListAPIView):
    serializer_class = SpendStatisticSerializer

    def get_queryset(self):
        queryset = SpendStatistic.objects.values("date", "name").annotate(
            total_spend=Sum("spend"),
            total_impressions=Sum("impressions"),
            total_clicks=Sum("clicks"),
            total_conversion=Sum("conversion"),
            total_revenue=Sum("revenuestatistic__revenue")
        )
        return queryset
