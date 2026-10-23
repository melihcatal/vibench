from typing import List
from mindee import MindeeClient, InvoiceV4

MINDEE_API_KEY = os.getenv("MINDEE_API_KEY")
client = MindeeClient(MINDEE_API_KEY)

def extract_invoice_fields(text: str) -> dict:
    """Simple placeholder; real implementation would parse Mindee output.",
    return {}
