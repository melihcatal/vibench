from storage_client import get_bucket, raise_storage_error
from storage_models import ListedObject, ListPrefixResponse, isoformat, to_dict


def list_prefix(bucket: str, prefix: str = "", max_keys: int = 1000):
    try:
        objs = []
        for obj in get_bucket(bucket).objects.filter(Prefix=prefix).limit(max_keys):
            objs.append(
                ListedObject(
                    key=obj.key,
                    size=getattr(obj, "size", None),
                    last_modified=isoformat(getattr(obj, "last_modified", None)),
                    etag=getattr(obj, "e_tag", None),
                )
            )
        response = ListPrefixResponse(bucket=bucket, prefix=prefix, objects=objs)
        return to_dict(response)
    except Exception as exc:
        raise raise_storage_error(exc)
