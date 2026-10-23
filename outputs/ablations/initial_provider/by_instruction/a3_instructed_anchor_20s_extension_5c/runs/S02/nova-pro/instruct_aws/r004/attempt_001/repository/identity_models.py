from typing import Dict

def normalize_user_attributes(attributes: Dict):
    return {k.lower(): v for k, v in attributes.items()}