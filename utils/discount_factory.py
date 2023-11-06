from models.discount import BulkDiscount, BundleDiscount, ThreeForTwoDiscount


class DiscountFactory:
    """Factory for creating discount instances based on the configuration file."""

    @staticmethod
    def get_discount(rule):
        """Creates a discount instance based on the configuration file.

        Args:
            rule (dict): A dictionary containing the discount configuration.

        Raises:
            ValueError: If the discount type is unknown.

        Returns:
            Discount: A discount instance.
        """
        discount_type = rule.get("type")
        if discount_type == "ThreeForTwoDiscount":
            return ThreeForTwoDiscount(rule["sku"])
        elif discount_type == "BulkDiscount":
            return BulkDiscount(
                rule["sku"], rule["threshold"], rule["discounted_price"]
            )
        elif discount_type == "BundleDiscount":
            return BundleDiscount(
                rule["sku"], rule["free_sku"]
            )
        else:
            raise ValueError(f"Unknown discount type: {discount_type}")
