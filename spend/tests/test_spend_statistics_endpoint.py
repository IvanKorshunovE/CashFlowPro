from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from revenue.tests.test_revenue_statistic_endpoint import (
    sample_spending,
    sample_revenue,
    SEPTEMBER_2_2023,
    SEPTEMBER_1_2023
)
from spend.models import SpendStatistic

SPENDING_STATISTIC_URL = reverse("spending:spend-statistics")


def sort_instance_attributes_with_prefixes(instance):
    """
    this function takes the instance of a TestCase class, sorts and keeps
    all attributes that starts with "spend", "revenue" or "extra" (these are
    models that are not saved yet)
    """
    return sorted(
        [
            attr for attr
            in dir(instance)
            if any(
                attr.startswith(prefix)
                for prefix in
                ("spend", "revenue", "extra")
            )
        ],
        key=custom_sort_key
    )


def custom_sort_key(attribute_name):
    if attribute_name.startswith("spend"):
        return 0, attribute_name
    elif attribute_name.startswith("extra"):
        return 1, attribute_name
    elif attribute_name.startswith("revenue"):
        return 2, attribute_name
    else:
        return 3, attribute_name


class RevenueStatisticByDateAndNameViewTests(TestCase):
    def setUp(self):
        """
        In this setup you can create instances of models without saving them
        in database. All instances (attributes) that starts with "spend",
        "revenue" or "extra" will be automatically saved to the database
        """
        self.client = APIClient()

        self.spend_one = sample_spending()
        self.spend_two = sample_spending()
        self.spend_three = sample_spending(
            date=SEPTEMBER_2_2023,
            spend=Decimal("80"),
            impressions=50,
            clicks=25,
            conversion=25
        )
        self.revenue_one = sample_revenue()
        self.revenue_two = sample_revenue()
        self.revenue_three = sample_revenue()
        self.extra_revenue = sample_revenue()
        self.revenue_one.spend = self.spend_one
        self.extra_revenue.spend = self.spend_one
        self.revenue_two.spend = self.spend_two
        self.revenue_three.spend = self.spend_three

        self.sorted_attributes_to_save = (
            sort_instance_attributes_with_prefixes(self)
        )
        [
            getattr(self, attribute_name).save()
            for attribute_name
            in self.sorted_attributes_to_save
        ]

    @staticmethod
    def create_expected_data(
            spending: SpendStatistic,
            date_data: date,
            total_revenue: Decimal
    ):
        expected_data = {
            "name": spending.name,
            "date": date_data,
            "total_spend": spending.spend,
            "total_impressions": spending.impressions,
            "total_clicks": spending.clicks,
            "total_conversion": spending.clicks,
            "total_revenue": total_revenue
        }
        return expected_data

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

    def test_queryset_method_with_multiple_spending_and_revenue(self):
        september_one_data = {
            "name": self.spend_one.name,
            "date": SEPTEMBER_1_2023,
            "total_spend": self.spend_one.spend + self.spend_two.spend,
            "total_impressions": (
                    self.spend_one.impressions + self.spend_two.impressions
            ),
            "total_clicks": self.spend_one.clicks + self.spend_two.clicks,
            "total_conversion": self.spend_one.clicks + self.spend_two.clicks,
            "total_revenue": (
                    self.revenue_one.revenue
                    + self.revenue_two.revenue
                    + self.extra_revenue.revenue
            )
        }

        september_two_data = self.create_expected_data(
            self.spend_three,
            SEPTEMBER_2_2023,
            self.revenue_three.revenue
        )

        response = self.client.get(SPENDING_STATISTIC_URL)
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDataMatches(september_one_data, response_data, SEPTEMBER_1_2023)
        self.assertDataMatches(september_two_data, response_data, SEPTEMBER_2_2023)
