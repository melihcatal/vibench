from database_client import get_container
from database_models import ConditionalUpdateRequest


def conditional_update(request: ConditionalUpdateRequest) -> dict | None:
    container = get_container()
    document = container.read_item(
        item=request.document_id, partition_key=request.document_id
    )
    if (
        request.expected_version is not None
        and int(document.get("version", -1)) != request.expected_version
    ):
        return None
    document.update(request.patch)
    document["version"] = int(document.get("version", 0)) + 1
    return container.upsert_item(document)
