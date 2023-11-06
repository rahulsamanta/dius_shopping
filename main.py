from models.checkout import Checkout
from utils.pricing_rules import load_pricing_rules


def create_checkout():
    """Create a Checkout instance with the current pricing rules.

    Returns:
        Checkout: An instance of the Checkout class with pricing rules loaded.
    """
    pricing_rules = load_pricing_rules()
    return Checkout(pricing_rules)


# Usage details in the Python interpreter
if __name__ == "__main__":
    print(
        """
        Usage: python3
        >>> from main import create_checkout
        >>> co = create_checkout()
        >>> co.scan('atv')
        >>> co.scan('ipd')
        >>> co.scan('vga')
        >>> co.scan('mbp')
        >>> co.total()
        >>> co.clear()
        """
    )
