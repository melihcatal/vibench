from typing import Dict, Any, List, Tuple


def validate_document_fields(
    normalized_data: Dict[str, Any], required_fields: List[str]
) -> Tuple[bool, List[str]]:
    missing_fields = []
    for field in required_fields:
        if field not in normalized_data or not normalized_data.get(field):
            missing_fields.append(field)
        elif field == "items" and len(normalized_data.get(field, [])) == 0:
            missing_fields.append(field)

    if normalized_data.get("confidence_score", 0) < 0.7:
        missing_fields.append("confidence_score_below_threshold")

    return (len(missing_fields) == 0, missing_fields)
