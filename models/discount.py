from typing import Literal


class Discount:
    """A base discount class from which all types of discounts will inherit."""

    def apply(self, items: list):
        """Applies the discount strategy to the given items.

        Args:
            items (list): A list of Product instances.

        Returns:
            float: The total discount amount.
        """
        raise NotImplementedError("Subclasses must override this method.")


class ThreeForTwoDiscount(Discount):
    """A discount that applies a 'three for the price of two' deal on a product."""

    def __init__(self, sku: str):
        """Initialize the ThreeForTwoDiscount.

        Args:
            sku (str): The SKU of the product to apply the discount to.
        """
        self.sku = sku

    def apply(self, items: list) -> (float | Literal[0]):
        """Applies the 'three for the price of two' discount to the items.

        Args:
            items (list): A list of Product instances.

        Returns:
            float: The total discount amount.
        """
        applicable_items = [item for item in items if item.sku == self.sku]
        free_items_count = len(applicable_items) // 3
        if free_items_count > 0:
            item_price = applicable_items[0].price
            return free_items_count * item_price
        return 0


class BulkDiscount(Discount):
    """A discount that applies a new price to items when bought in bulk."""

    def __init__(self, sku: str, threshold: int, discounted_price: float):
        """Initializes a new instance of the BulkDiscount class.

        Args:
            sku (str): The SKU of the product to which the discount applies.
            threshold (int): The quantity threshold for the discount to apply.
            discounted_price (float): The new price when the threshold is reached.
        """
        self.sku = sku
        self.threshold = threshold
        self.discounted_price = discounted_price

    def apply(self, items: list) -> (float | Literal[0]):
        """Applies the bulk discount to items if applicable.

        Args:
            items (list): A list of Product instances.

        Returns:
            float: The total discount amount.
        """
        applicable_items = [item for item in items if item.sku == self.sku]
        if len(applicable_items) > self.threshold:
            discount = sum(
                item.price for item in applicable_items
            ) - (len(applicable_items) * self.discounted_price)
            return discount
        return 0


class BundleDiscount(Discount):
    """A discount that bundles a free product with each purchase of another."""

    def __init__(self, sku: str, free_sku: str):
        """Initializes a new instance of the BundleDiscount class.

        Args:
            sku (str): The SKU of the product that must be bought to get another free.
            free_sku (str): The SKU of the product that is bundled for free.
        """
        self.sku = sku
        self.free_sku = free_sku

    def apply(self, items: list) -> (float | Literal[0]):
        """Applies the bundle discount to items if applicable.

        Args:
            items (list): A list of Product instances.

        Returns:
            float: The total discount amount.
        """
        required_items_count = sum(1 for item in items if item.sku == self.sku)
        free_items = [item for item in items if item.sku == self.free_sku]

        paired_free_items = 0
        discount = 0

        for _ in range(required_items_count):
            if paired_free_items < len(free_items):
                discount += free_items[paired_free_items].price
                paired_free_items += 1

        return discount
