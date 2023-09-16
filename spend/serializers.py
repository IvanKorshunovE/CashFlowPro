from rest_framework import serializers

from spend.models import SpendStatistic


class SpendStatisticSerializer(serializers.ModelSerializer):
    total_spend = serializers.IntegerField()
    total_impressions = serializers.IntegerField()
    total_clicks = serializers.IntegerField()
    total_conversion = serializers.IntegerField()
    total_revenue = serializers.IntegerField()

    class Meta:
        model = SpendStatistic
        fields = (
            "name",
            "date",
            "total_spend",
            "total_impressions",
            "total_clicks",
            "total_conversion",
            "total_revenue",
        )
