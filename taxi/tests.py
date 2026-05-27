from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car


class SearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123",
            license_number="ABC12456"
        )
        self.client.force_login(self.user)

    def test_search_manufacturers_by_name(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")

        response = self.client.get(reverse(
            "taxi:manufacturer-list") + "?name=Toy"
        )

        self.assertEqual(response.status_code, 200)

    def test_search_cars_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="Honda",
            country="Japan"
        )

        Car.objects.create(
            model="Civic",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="Accord",
            manufacturer=manufacturer
        )

        response = self.client.get(reverse(
            "taxi:car-list") + "?model=Civ"
        )

        self.assertEqual(response.status_code, 200)

    def test_search_drivers_by_username(self):
        get_user_model().objects.create_user(
            username="johndoe",
            password="123",
            license_number="XYZ98765"
        )

        response = self.client.get(reverse(
            "taxi:driver-list") + "?username=john"
        )

        self.assertEqual(response.status_code, 200)
