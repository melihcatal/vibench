from database_client import get_collection_name, get_firestore_client
from database_models import build_record_result


def conditional_update(payload, config=None):
    config = config or {}
    client = get_firestore_client(config)
    ref = client.collection(get_collection_name(config)).document(payload["id"])
    snapshot = ref.get()
    current = snapshot.to_dict() if snapshot.exists else {}
    expected_version = payload.get("expected_version")
    if expected_version is not None and current.get("version") != expected_version:
        return {"id": payload["id"], "updated": False, "document": current}
    updated = dict(current)
    updated.update(payload["updates"])
    if "version" in current or expected_version is not None:
        updated["version"] = (current.get("version") or 0) + 1
    ref.set(updated)
    return {"id": payload["id"], "updated": True, "document": build_record_result(payload["id"], updated)["document"]}
