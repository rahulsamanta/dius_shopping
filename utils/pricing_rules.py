import json
from pathlib import Path

from utils.discount_factory import DiscountFactory

PRICING_RULES_PATH = (
    Path(__file__).parent.parent / 'config' / 'pricing_rules.json'
)


def load_pricing_rules() -> list:
    """Load the pricing rules from the external configuration file.

    Returns:
        list: A list of Discount instances created based on the configuration file.
    """
    try:
        with open(PRICING_RULES_PATH, 'r') as config_file:
            rules_config = json.load(config_file)

        for index, rule in enumerate(rules_config):
            if 'type' not in rule or 'sku' not in rule:
                raise ValueError(f"Rule at index {index} must contain 'type' and 'sku'.")
            if rule['type'] == 'BulkDiscount' and (
                    'threshold' not in rule or 'discounted_price' not in rule
            ):
                raise ValueError(
                    "BulkDiscount rules must contain 'threshold' and 'discounted_price'."
                )
            if rule['type'] == 'BundleDiscount' and ('free_sku' not in rule):
                raise ValueError(
                    "BundleDiscount rules must contain 'free_sku'."
                )

        pricing_rules = []
        for rule in rules_config:
            discount = DiscountFactory.get_discount(rule)
            pricing_rules.append(discount)

        return pricing_rules

    except json.JSONDecodeError as json_error:
        print(f"Error: The pricing rules file contains invalid JSON. {json_error}")
        raise
    except ValueError as value_error:
        print(f"Error in pricing rules configuration: {value_error}")
        raise
