from django.test import Client, TestCase
from django.urls import reverse

from .models import Customer, Order, OrderItem, Product, ShippingAdress


class TestModels(TestCase):

    def setUp(self):
        self.customer1 = Customer.objects.create(
            name="customer1", email="customer1@example.com"
        )

        self.product1 = Product.objects.create(
            name="product1", price=100.00, digital=False
        )

        self.order1 = Order.objects.create(customer=self.customer1, complete=False)

        self.orderitem1 = OrderItem.objects.create(
            product=self.product1, order=self.order1, quantity=1
        )

        self.shippingaddress1 = ShippingAdress.objects.create(
            customer=self.customer1,
            order=self.order1,
            address="123 St",
            state="State",
            zipcode="12345",
            city="City",
        )

    def test_customer_creation(self):
        self.assertEqual(self.customer1.name, "customer1")
        self.assertEqual(self.customer1.email, "customer1@example.com")

    def test_product_creation(self):
        self.assertEqual(self.product1.name, "product1")
        self.assertEqual(self.product1.price, 100.00)
        self.assertEqual(self.product1.digital, False)

    def test_order_creation(self):
        self.assertEqual(self.order1.customer, self.customer1)
        self.assertEqual(self.order1.complete, False)

    def test_orderitem_creation(self):
        self.assertEqual(self.orderitem1.product, self.product1)
        self.assertEqual(self.orderitem1.order, self.order1)
        self.assertEqual(self.orderitem1.quantity, 1)

    def test_shippingaddress_creation(self):
        self.assertEqual(self.shippingaddress1.customer, self.customer1)
        self.assertEqual(self.shippingaddress1.order, self.order1)
        self.assertEqual(self.shippingaddress1.address, "123 St")
        self.assertEqual(self.shippingaddress1.state, "State")
        self.assertEqual(self.shippingaddress1.zipcode, "12345")
        self.assertEqual(self.shippingaddress1.city, "City")


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.store_url = reverse("store")
        self.cart_url = reverse("cart")
        self.checkout_url = reverse("checkout")
        self.product1 = Product.objects.create(
            name="product1", price=100.00, digital=False
        )

    def test_store_GET(self):
        response = self.client.get(self.store_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "store/store.html")

    def test_cart_GET(self):
        response = self.client.get(self.cart_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "store/cart.html")

    def test_checkout_GET(self):
        response = self.client.get(self.checkout_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "store/checkout.html")
