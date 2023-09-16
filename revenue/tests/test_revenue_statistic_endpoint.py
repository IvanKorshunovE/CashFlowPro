from datetime import date
from decimal import Decimal

from django.test import TestCase

from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from revenue.models import RevenueStatistic
from spend.models import SpendStatistic

REVENUE_STATISTIC_URL = reverse("revenue:revenue-statistics")
SEPTEMBER_1_2023 = date(2023, 9, 1)
SEPTEMBER_2_2023 = date(2023, 9, 2)


def sample_spending(**params) -> SpendStatistic:
    """
    Function for creating test
    SpendStatistic object
    """
    spend_sum = Decimal("50")

    defaults = {
        "name": "Test Spend",
        "date": SEPTEMBER_1_2023,
        "spend": spend_sum,
        "impressions": 10,
        "clicks": 10,
        "conversion": 10
    }
    defaults.update(params)

    return SpendStatistic(**defaults)


def sample_revenue(**params) -> RevenueStatistic:
    """
    Function for creating test
    RevenueStatistic object
    """
    revenue_sum = Decimal("100")

    defaults = {
        "name": "Test Revenue",
        "spend": None,
        "date": SEPTEMBER_1_2023,
        "revenue": revenue_sum
    }
    defaults.update(params)

    return RevenueStatistic(**defaults)


class RevenueStatisticByDateAndNameViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    @staticmethod
    def create_expected_data(
            revenue: RevenueStatistic,
            date_data: date
    ):
        expected_data = {
            "name": revenue.name,
            "date": date_data,
            "total_revenue": revenue.revenue,
            "total_spend": revenue.spend.spend,
            "total_impressions": revenue.spend.impressions,
            "total_clicks": revenue.spend.clicks,
            "total_conversion": revenue.spend.conversion
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
            Decimal(found_data.get("total_revenue")),
            expected_data["total_revenue"]
        )
        self.assertEqual(
            Decimal(found_data.get("total_spend")),
            expected_data["total_spend"]
        )
        self.assertEqual(
            Decimal(found_data.get("total_impressions")),
            expected_data["total_impressions"]
        )
        self.assertEqual(
            found_data.get("total_clicks"),
            expected_data["total_clicks"]
        )
        self.assertEqual(
            found_data.get("total_conversion"),
            expected_data["total_conversion"]
        )

    def test_queryset_method_with_one_revenue_and_spending(self):
        """
        This method tests the behaviour of the get_queryset method
        when we have one revenue and one spending
        """
        spend_one = sample_spending()
        revenue_one = sample_revenue()
        revenue_one.spend = spend_one
        spend_one.save()
        revenue_one.save()

        revenue_data = self.create_expected_data(revenue_one, SEPTEMBER_1_2023)
        response = self.client.get(REVENUE_STATISTIC_URL)
        response_data = response.data

        self.assertDataMatches(revenue_data, response_data)

    def test_queryset_method_with_multiple_revenue_and_spending(self):
        """
        This method tests the behaviour of the get_queryset method
        when we have multiple revenue and multiple spending
        """
        spend_one = sample_spending()
        spend_two = sample_spending()
        spend_three = sample_spending(
            spend=Decimal("112"),
            impressions=112,
            clicks=112
        )

        revenue_one = sample_revenue()
        revenue_two = sample_revenue()
        revenue_three = sample_revenue(
            date=SEPTEMBER_2_2023
        )

        revenue_one.spend = spend_one
        revenue_two.spend = spend_two
        revenue_three.spend = spend_three

        spend_one.save()
        spend_two.save()
        spend_three.save()

        revenue_one.save()
        revenue_two.save()
        revenue_three.save()

        september_one_data = {
            "name": revenue_one.name,
            "date": SEPTEMBER_1_2023,
            "total_revenue": revenue_one.revenue + revenue_two.revenue,
            "total_spend": revenue_one.spend.spend + revenue_two.spend.spend,
            "total_impressions": revenue_one.spend.impressions + revenue_two.spend.impressions,
            "total_clicks": revenue_one.spend.clicks + revenue_two.spend.clicks,
            "total_conversion": revenue_one.spend.conversion + revenue_two.spend.conversion
        }

        september_two_data = self.create_expected_data(revenue_three, SEPTEMBER_2_2023)

        response = self.client.get(REVENUE_STATISTIC_URL)
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDataMatches(september_one_data, response_data, SEPTEMBER_1_2023)
        self.assertDataMatches(september_two_data, response_data, SEPTEMBER_2_2023)
