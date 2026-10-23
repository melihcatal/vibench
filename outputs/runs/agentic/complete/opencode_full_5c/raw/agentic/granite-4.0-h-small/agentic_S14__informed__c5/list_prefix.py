import os
from storage_client import (
    get_s3_client,
    get_gcloud_storage_client,
    get_azure_blob_client,
    get_b2_client,
    get_oss_client,
    get_cos_client,
)
from storage_models import ListPrefixResponse


def list_prefix(**kwargs):
    """
    List objects under a bucket/prefix with continuation support.
    Provider selected via PROVIDER env var.
    Required kwargs:
      bucket_name
      prefix
    Optional kwargs:
      max_keys (default 1000)
      continuation_token
    Returns ListPrefixResponse.
    """
    provider = os.getenv("PROVIDER")
    bucket = kwargs["bucket_name"]
    prefix = kwargs.get("prefix", "")
    max_keys = kwargs.get("max_keys", 1000)
    continuation_token = kwargs.get("continuation_token")

    if provider == "s3":
        client = get_s3_client()
        resp = client.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix,
            MaxKeys=max_keys,
            ContinuationToken=continuation_token,
        )
        contents = [
            dict(
                Key=obj["Key"],
                Size=obj.get("Size", 0),
                ETag=obj.get("ETag", "").strip('"'),
                ContentType=obj.get("ContentType", ""),
                LastModified=obj.get("LastModified", "").isoformat(),
            )
            for obj in resp.get("Contents", [])
        ]
        return ListPrefixResponse(
            bucket_name=bucket,
            prefix=prefix,
            continuation_token=resp.get("NextContinuationToken"),
            contents=contents,
        )
    elif provider == "gcs":
        client = get_gcloud_storage_client()
        blobs = list(
            client.bucket(bucket).list_blobs(
                prefix=prefix,
                max_results=max_keys,
                delimiter=None,
                start_offset=continuation_token,
            )
        )
        contents = [
            dict(
                name=blob.name,
                size=blob.size,
                etag=blob.etag.strip('"'),
                contentType=blob.content_type,
                updated=blob.updated.isoformat(),
            )
            for blob in blobs
        ]
        return ListPrefixResponse(
            bucket_name=bucket,
            prefix=prefix,
            continuation_token=blob.page_token,
            contents=contents,
        )
    elif provider == "azure":
        client = get_azure_blob_client()
        blob_service_client = client.get_blob_service_client()
        container_client = blob_service_client.get_container_client(bucket)
        blobs = list(
            container_client.list_blobs(
                name_starts_with=prefix, max_results=max_keys, prefix=prefix
            )
        )
        contents = [
            dict(
                name=blob.name,
                size=blob.size,
                etag=blob.properties.etag,
                contentType=blob.properties.content_type,
                lastModified=blob.properties.last_modified.isoformat(),
            )
            for blob in blobs
        ]
        return ListPrefixResponse(
            bucket_name=bucket,
            prefix=prefix,
            continuation_token=None,
            contents=contents,
        )
    elif provider == "b2":
        client = get_b2_client()
        bucket_id = client.get_bucket_id(bucket)
        resp = client.list_file_names(
            bucket_id,
            prefix=prefix,
            max_file_count=max_keys,
            start_file_name=continuation_token,
        )
        contents = [
            dict(
                fileName=f["fileName"],
                size=f["size"],
                sha1=f["sha1"],
                contentType=f["contentType"],
                uploadTimestamp=f["uploadTimestamp"].isoformat(),
            )
            for f in resp.get("files", [])
        ]
        return ListPrefixResponse(
            bucket_name=bucket,
            prefix=prefix,
            continuation_token=resp.get("nextFileName", None),
            contents=contents,
        )
    elif provider == "oss":
        client = get_oss_client()
        resp = client.list_objects(
            prefix=prefix, max_keys=max_keys, marker=continuation_token
        )
        contents = [
            dict(
                key=obj.key,
                size=obj.size,
                etag=obj.etag,
                type=obj.type,
                lastModified=obj.last_modified.isoformat(),
            )
            for obj in resp.object_list
        ]
        return ListPrefixResponse(
            bucket_name=bucket,
            prefix=prefix,
            continuation_token=resp.next_marker,
            contents=contents,
        )
    elif provider == "cos":
        client = get_cos_client()
        resp = client.get_object_listing(
            bucket, prefix=prefix, max_keys=max_keys, start=continuation_token
        )
        contents = [
            dict(
                Key=obj["Key"],
                Size=obj["Size"],
                ETag=obj.get("ETag", ""),
                ContentType=obj.get("ContentType", ""),
                LastModified=obj.get("LastModified", ""),
            )
            for obj in resp.get("Contents", [])
        ]
        return ListPrefixResponse(
            bucket_name=bucket,
            prefix=prefix,
            continuation_token=resp.get("NextContinuationToken"),
            contents=contents,
        )
    else:
        raise ValueError(f"Unsupported provider {provider}")
