from rest_framework import serializers

from revenue.models import RevenueStatistic


class RevenueStatisticSerializer(serializers.ModelSerializer):
    total_revenue = serializers.IntegerField()
    total_spend = serializers.IntegerField()
    total_impressions = serializers.IntegerField()
    total_clicks = serializers.IntegerField()
    total_conversion = serializers.IntegerField()

    class Meta:
        model = RevenueStatistic
        fields = (
            "name",
            "date",
            "revenue",
            "total_revenue",
            "total_spend",
            "total_impressions",
            "total_clicks",
            "total_conversion",
        )
