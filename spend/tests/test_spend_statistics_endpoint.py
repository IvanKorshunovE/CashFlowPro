from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from revenue.tests.test_revenue_statistic_endpoint import (
    sample_spending,
    sample_revenue,
    SEPTEMBER_2_2023, SEPTEMBER_1_2023
)

SPENDING_STATISTIC_URL = reverse("spending:spend-statistics")


class RevenueStatisticByDateAndNameViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def assertDataMatches(
            self,
            expected_data: dict,
            response_data: dict,
            date_key: date = SEPTEMBER_1_2023
    ):
        found_data = None
        for data in response_data:
            if data["date"] == str(date_key):
                found_data = data
                break

        self.assertIsNotNone(found_data)

        self.assertEqual(
            Decimal(found_data.get("total_spend")),
            expected_data["total_spend"]
        )
        self.assertEqual(
            Decimal(found_data.get("total_impressions")),
            expected_data["total_impressions"]
        )
        self.assertEqual(
            Decimal(found_data.get("total_clicks")),
            expected_data["total_clicks"]
        )
        self.assertEqual(
            found_data.get("total_conversion"),
            expected_data["total_conversion"]
        )
        self.assertEqual(
            found_data.get("total_revenue"),
            expected_data["total_revenue"]
        )

    def test_queryset_method_with_multiple_spendings_and_revenue(self):
        spend_one = sample_spending()
        spend_two = sample_spending()
        spend_three = sample_spending(
            date=SEPTEMBER_2_2023,
            spend=Decimal("80"),
            impressions=50,
            clicks=25,
            conversion=25
        )

        revenue_one = sample_revenue()
        revenue_two = sample_revenue()
        revenue_three = sample_revenue()
        extra_revenue = sample_revenue()

        revenue_one.spend = spend_one
        extra_revenue.spend = spend_one
        revenue_two.spend = spend_two
        revenue_three.spend = spend_three

        spend_one.save()
        spend_two.save()
        spend_three.save()

        revenue_one.save()
        revenue_two.save()
        revenue_three.save()
        extra_revenue.save()

        september_one_data = {
            "name": spend_one.name,
            "date": SEPTEMBER_1_2023,
            "total_spend": spend_one.spend + spend_two.spend,
            "total_impressions": spend_one.impressions + spend_two.impressions,
            "total_clicks": spend_one.clicks + spend_two.clicks,
            "total_conversion": spend_one.clicks + spend_two.clicks,
            "total_revenue": revenue_one.revenue + revenue_two.revenue + extra_revenue.revenue
        }

        response = self.client.get(SPENDING_STATISTIC_URL)
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDataMatches(september_one_data, response_data, SEPTEMBER_1_2023)
