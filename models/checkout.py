from typing import List
from .discount import Discount
from utils.product_catalogue import load_product_catalogue


class Checkout:
    """A checkout system that handles scanning items and calculating the total price with discounts."""

    def __init__(self, pricing_rules: List[Discount]):
        """Initialize the Checkout system with the given pricing rules and load the product catalog.

        Args:
            pricing_rules (List[Discount]): A list of pricing rules to be applied.
        """
        self.product_catalogue = load_product_catalogue()
        self.pricing_rules = pricing_rules
        self.items = []

    def scan(self, sku: str):
        """Scan a product by SKU, adding it to the list of items.

        Args:
            sku (str): The SKU of the product to be scanned.

        Raises:
            ValueError: If a product with the given SKU does not exist.
        """
        product = self.product_catalogue.get(sku)
        if not product:
            raise ValueError(f"Product with SKU '{sku}' not found.")
        self.items.append(product)

    def total(self) -> float:
        """Calculate the total price for all scanned items with discounts applied.

        Returns:
            float: The total price for all items.
        """
        total_price = sum(item.price for item in self.items)
        total_discount = sum(rule.apply(self.items) for rule in self.pricing_rules)
        return total_price - total_discount

    def clear(self):
        """Clear all scanned items."""
        self.items = []
