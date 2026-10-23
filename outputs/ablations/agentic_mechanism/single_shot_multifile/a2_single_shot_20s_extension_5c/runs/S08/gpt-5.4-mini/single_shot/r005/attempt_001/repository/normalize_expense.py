import json
from typing import Any, Dict

from document_models import normalize_expense_record


def normalize_expense(extracted_fields: Any) -> Dict[str, Any]:
    if isinstance(extracted_fields, str):
        try:
            extracted_fields = json.loads(extracted_fields)
        except json.JSONDecodeError:
            extracted_fields = {"raw_text": extracted_fields}
    return normalize_expense_record(extracted_fields)


if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    print(json.dumps(normalize_expense(data), ensure_ascii=False))
