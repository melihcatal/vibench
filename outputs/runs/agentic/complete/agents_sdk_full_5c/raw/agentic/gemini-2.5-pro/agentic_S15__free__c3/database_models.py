from decimal import Decimal
import json

class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert a DynamoDB item to JSON."""
    def default(self, o):
        if isinstance(o, Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def prepare_document_for_db(doc: dict) -> dict:
    """
    Recursively converts floats to Decimals for DynamoDB compatibility.
    """
    # This is a simple implementation. A more robust one would handle nested structures.
    return json.loads(json.dumps(doc), parse_float=Decimal)

def normalize_document_from_db(item: dict) -> dict:
    """
    Converts a DynamoDB item (with Decimals) to a standard JSON-compatible dict.
    """
    return json.loads(json.dumps(item, cls=DecimalEncoder))
