from storage_client import get_storage_client
from storage_models import ListPrefixRequest, ListedObject


def list_prefix(request: ListPrefixRequest):
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)
    blobs = client.list_blobs(
        bucket, prefix=request.prefix, delimiter=request.delimiter
    )

    objects = []
    for blob in blobs:
        objects.append(
            ListedObject(
                name=blob.name, size=blob.size, updated=blob.updated.isoformat()
            )
        )

    prefixes = []
    if request.delimiter:
        for page in blobs.pages:
            prefixes.extend(page.prefixes)

    return {"objects": objects, "prefixes": prefixes}
