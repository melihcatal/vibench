import json
from typing import Dict, Any
from database_client import client
from database_models import ConditionalUpdate, DocumentResponse


def conditional_update(update: ConditionalUpdate) -> DocumentResponse:
    """
    Performs a version‑aware (optimistic) update on a single document.
    The `condition` string is evaluated against the current document metadata.
    Example condition: "version == 5".
    If the condition fails, raises RuntimeError.
    """
    coll = client.get_collection()  # concrete provider call (e.g., pymongo.Collection)
    # Retrieve current document and version
    current = coll.find_one({"id": update["condition"].split("==")[1].strip()})
    if not current:
        raise RuntimeError("Document not found for conditional update")
    current_version = current.get("version", 0)
    expected_expr = update["condition"]
    try:
        # Simple equality check for demonstration
        if not eval(expected_expr, {}, current):
            raise RuntimeError(f"Conditional check failed: {expected_expr}")
    except Exception as e:
        raise RuntimeError(f"Error evaluating condition '{expected_expr}': {e}")
    # Apply updates (merge with existing fields)
    new_data = {**current.get("data", {}), **update["updates"]}
    coll.replace_one(
        {"id": current["id"]},
        {"id": current["id"], "data": new_data, "version": current_version + 1},
        upsert=False,
    )
    # Return the updated representation
    return DocumentResponse(
        id=current["id"], data=new_data, version=current_version + 1
    )


# Demo/CLI entry point
if __name__ == "__main__":
    demo_update = {
        "condition": "version == 0",
        "updates": {"title": "Updated Title", "extra": "field"},
    }
    try:
        result = conditional_update(demo_update)
        print(json.dumps(result, indent=2))
    except RuntimeError as e:
        print(e)
