import os
from typing import Any, Dict

from pinecone import Pinecone


def profile_note_store(event: Dict[str, Any]) -> Dict[str, Any]:
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY", ""))
    index = pc.Index(os.getenv("PINECONE_INDEX", "onboarding-notes"))
    namespace = str(event.get("namespace", "default")).strip() or "default"
    note_id = str(event.get("note_id", "")).strip() or "note"
    metadata = dict(event.get("metadata", {}))
    vector = event.get("vector", [0.0])
    index.upsert(
        vectors=[{"id": note_id, "values": vector, "metadata": metadata}],
        namespace=namespace,
    )
    return {"stored": True, "note_id": note_id, "namespace": namespace}
