from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Driver, Car, Manufacturer

User = get_user_model()


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="john",
            password="pass12345",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
        )

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "john (John Doe)")


class ManufacturerModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), "Toyota Japan")


class CarModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer,
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), "Camry")


class DriverCRUDTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="john",
            password="pass12345",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
        )
        self.client.login(username="john", password="pass12345")

    def test_driver_list(self):
        self.client.get(reverse("taxi:driver-list"))

    def test_driver_create(self):
        self.client.post(
            reverse("taxi:driver-create"),
            {
                "username": "mike",
                "password1": "pass12345",
                "password2": "pass12345",
                "license_number": "DEF67890",
                "first_name": "Mike",
                "last_name": "Smith",
            },
        )
        self.assertEqual(Driver.objects.filter(username="mike").count(), 1)


class ManufacturerCRUDTest(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="john",
            password="pass12345",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
        )
        self.client.login(username="john", password="pass12345")
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

    def test_manufacturer_list(self):
        self.client.get(reverse("taxi:manufacturer-list"))

    def test_manufacturer_create(self):
        self.client.post(
            reverse("taxi:manufacturer-create"),
            {"name": "Honda", "country": "Japan"},
        )
        self.assertEqual(Manufacturer.objects.filter(name="Honda").count(), 1)


class CarCRUDTest(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="john",
            password="pass12345",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
        )
        self.client.login(username="john", password="pass12345")
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

    def test_car_list(self):
        Car.objects.create(model="Camry", manufacturer=self.manufacturer)
        self.client.get(reverse("taxi:car-list"))

    def test_car_create(self):
        self.client.post(
            reverse("taxi:car-create"),
            {
                "model": "Camry",
                "manufacturer": self.manufacturer.id,
                "drivers": [],
            },
        )
        self.assertEqual(Car.objects.filter(model="Camry").count(), 1)

    def test_car_update(self):
        car = Car.objects.create(model="OldModel",
                                 manufacturer=self.manufacturer
                                 )
        self.client.post(
            reverse("taxi:car-update", args=[car.id]),
            {
                "model": "NewModel",
                "manufacturer": self.manufacturer.id,
                "drivers": [],
            },
        )
        car.refresh_from_db()
        self.assertEqual(car.model, "NewModel")
