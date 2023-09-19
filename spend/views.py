from django.db import connections
from drf_spectacular.utils import extend_schema
from rest_framework import generics

from spend.models import SpendStatistic
from spend.serializers import SpendStatisticSerializer


class SpendStatisticByDateAndNameView(generics.ListAPIView):
    serializer_class = SpendStatisticSerializer

    @staticmethod
    def create_spend_revenue_view():
        sql_create_view = """
            CREATE VIEW spend_revenue AS
            SELECT rev.spend_id, SUM(rev.revenue) AS total_revenue
            FROM revenue_revenuestatistic as rev
            GROUP BY rev.spend_id;
        """
        view_exists = """
            SELECT EXISTS(
                SELECT *
                FROM main.sqlite_master
                WHERE name = %s
            );
        """
        with connections["default"].cursor() as cursor:
            try:
                cursor.execute(view_exists, ("spend_revenue",))
                view_exists = cursor.fetchone()
                view_exists = view_exists[0]
                if not view_exists:
                    cursor.execute(sql_create_view)
            except Exception as e:
                print(f"Error creating view: {e}")

    def get_queryset(self):
        self.create_spend_revenue_view()
        queryset = SpendStatistic.objects.raw(
            """
            SELECT
                ss.id,
                ss.name AS name,
                ss.date AS date,
                SUM(ss.spend) AS total_spend,
                SUM(ss.impressions) AS total_impressions,
                SUM(ss.clicks) AS total_clicks,
                SUM(ss.conversion) AS total_conversion,
                COALESCE(SUM(sr.total_revenue), 0) AS total_revenue
            FROM spend_spendstatistic as ss
            LEFT JOIN spend_revenue as sr
            ON ss.id = sr.spend_id
            GROUP BY name, date;
            """
        )
        return queryset

    @extend_schema(
        description="Retrieve a list of spend statistics by date and name with aggregated data."
    )
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
