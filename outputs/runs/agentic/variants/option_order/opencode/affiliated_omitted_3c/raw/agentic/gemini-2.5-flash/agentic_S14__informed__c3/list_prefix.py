from storage_client import get_s3_client
from storage_models import ListPrefixRequest, ListPrefixResponse, ListedObject


def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    s3_client = get_s3_client()
    list_kwargs = {"Bucket": request.bucket_name, "MaxKeys": request.max_keys}
    if request.prefix:
        list_kwargs["Prefix"] = request.prefix

    response = s3_client.list_objects_v2(**list_kwargs)

    objects = []
    if "Contents" in response:
        for obj in response["Contents"]:
            objects.append(
                ListedObject(
                    key=obj["Key"],
                    last_modified=obj["LastModified"],
                    e_tag=obj["ETag"].strip('"'),
                    size=obj["Size"],
                )
            )

    common_prefixes = [p["Prefix"] for p in response.get("CommonPrefixes", [])]

    return ListPrefixResponse(objects=objects, common_prefixes=common_prefixes)
