from django.contrib import admin

from revenue.models import RevenueStatistic


@admin.register(RevenueStatistic)
class SpendStatisticAdmin(admin.ModelAdmin):
    list_display = ("name", "spend", "date", "revenue")

    def get_queryset(self, request):
        return RevenueStatistic.objects.select_related("spend")
