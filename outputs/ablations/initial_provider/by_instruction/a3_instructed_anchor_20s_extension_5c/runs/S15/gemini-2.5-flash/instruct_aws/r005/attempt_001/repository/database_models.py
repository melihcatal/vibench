def create_document(document_id: str, content: dict) -> dict:
    """
    Creates a standardized document structure.
    """
    return {"document_id": document_id, **content}

def normalize_item(item: dict) -> dict:
    """
    Normalizes a DynamoDB item to a simpler dictionary.
    """
    if not item:
        return {}
    return {k: v[list(v.keys())[0]] for k, v in item.items()}

def denormalize_item(item: dict) -> dict:
    """
    Denormalizes a simple dictionary to a DynamoDB item format.
    """
    dynamodb_item = {}
    for k, v in item.items():
        if isinstance(v, str):
            dynamodb_item[k] = {"S": v}
        elif isinstance(v, (int, float)):
            dynamodb_item[k] = {"N": str(v)}
        elif isinstance(v, bool):
            dynamodb_item[k] = {"BOOL": v}
        elif isinstance(v, list):
            if all(isinstance(x, str) for x in v):
                dynamodb_item[k] = {"L": [{"S": x} for x in v]}
            # Add more types as needed
        elif isinstance(v, dict):
            dynamodb_item[k] = {"M": denormalize_item(v)}
        elif v is None:
            dynamodb_item[k] = {"NULL": True}
    return dynamodb_item
