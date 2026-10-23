import os

def get_mindee_processor_type(service: str) -> str:
    """Return the Mindee processor name that matches the passed service name."""
    mapping = {
        "ocr": "ocr",
        "tables": "tables",
        "layout": "layout",
        "invoices": "invoices",
        "id_cards": "id_cards",
    }
    return mapping.get(service.lower(), "ocr")

_
