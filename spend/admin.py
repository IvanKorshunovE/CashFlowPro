from django.contrib import admin

from revenue.models import RevenueStatistic
from spend.models import SpendStatistic


class RevenueStatisticInline(admin.TabularInline):
    model = RevenueStatistic
    extra = 1


@admin.register(SpendStatistic)
class SpendStatisticAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "spend", "impressions", "clicks", "conversion")
    inlines = [RevenueStatisticInline]
