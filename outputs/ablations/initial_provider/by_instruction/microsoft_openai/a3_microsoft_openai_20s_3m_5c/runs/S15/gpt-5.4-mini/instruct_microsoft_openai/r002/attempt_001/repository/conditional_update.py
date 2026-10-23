from database_client import read_item, replace_item
from database_models import ConditionalUpdateRequest, normalize_document


def conditional_update(document_id, patch, version=None):
    request = ConditionalUpdateRequest(document_id=document_id, patch=patch, version=version)
    current = read_item(request.document_id)
    if request.version is not None and current.get("version") != request.version:
        return {"ok": False, "reason": "version_mismatch", "document": current}
    updated = normalize_document(current)
    updated.update(request.patch)
    if request.version is not None:
        updated["version"] = request.version + 1
    return replace_item(request.document_id, updated)
