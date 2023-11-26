from _decimal import Decimal
from django.core.management.base import BaseCommand
from webshop.models import Product

class Command(BaseCommand):
    help = 'Reduce the price of a selected product by a specified percentage'

    def add_arguments(self, parser):
        parser.add_argument('product_id', type=int, help='ID of the product to reduce the price')
        parser.add_argument('percentage', type=float, help='Percentage to reduce the price by')

    def handle(self, *args, **options):
        product_id = options['product_id']
        percentage = options['percentage']

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Product with ID {product_id} does not exist."))
            return

        original_price = product.product_price
        reduction_amount = (Decimal(percentage) / 100) * original_price
        new_price = original_price - reduction_amount

        product.product_price = new_price
        product.save()

        self.stdout.write(self.style.SUCCESS(
            f"Price of {product.product_name} (ID: {product_id}) reduced by {percentage}%.\n"
            f"Original Price: {original_price}\nNew Price: {new_price}"
        ))