import os
from storage_client import (
    get_s3_client,
    get_gcloud_storage_client,
    get_azure_blob_client,
    get_b2_client,
    get_oss_client,
    get_cos_client,
)
from storage_models import ObjectMetadata, ListPrefixResponse


def get_object_metadata(**kwargs):
    """
    Retrieve full metadata for a stored object.
    Provider selected via PROVIDER env var (same set as other helpers).
    Required kwargs:
      bucket_name
      object_key
    Returns ObjectMetadata.
    """
    provider = os.getenv("PROVIDER")
    bucket = kwargs["bucket_name"]
    key = kwargs["object_key"]
    if provider == "s3":
        client = get_s3_client()
        head = client.head_object(Bucket=bucket, Key=key)
        return ObjectMetadata(
            bucket_name=bucket,
            object_key=key,
            size=head["ContentLength"],
            etag=head["ETag"].strip('"'),
            content_type=head["ContentType"],
            last_modified=head["LastModified"].isoformat(),
        )
    elif provider == "gcs":
        client = get_gcloud_storage_client()
        blob = client.bucket(bucket).blob(key)
        metadata = blob.reload()  # retrieves metadata
        return ObjectMetadata(
            bucket_name=bucket,
            object_key=key,
            size=blob.size,
            etag=blob.etag.strip('"'),
            content_type=blob.content_type,
            last_modified=blob.updated.isoformat(),
        )
    elif provider == "azure":
        client = get_azure_blob_client()
        blob_service_client = client.get_blob_service_client()
        container_client = blob_service_client.get_container_client(bucket)
        blob_client = container_client.get_blob_client(key)
        props = blob_client.get_blob_properties()
        return ObjectMetadata(
            bucket_name=bucket,
            object_key=key,
            size=props.size,
            etag=props.etag,
            content_type=props.content_type,
            last_modified=props.last_modified.isoformat(),
        )
    elif provider == "b2":
        client = get_b2_client()
        bucket_id = client.get_bucket_id(bucket)
        meta = client.get_file_info(bucket_id, key)
        return ObjectMetadata(
            bucket_name=bucket,
            object_key=key,
            size=meta["size"],
            etag=meta["sha1"],  # simplified
            content_type=meta["contentType"],
            last_modified=meta["uploadTimestamp"].isoformat(),
        )
    elif provider == "oss":
        client = get_oss_client()
        meta = client.get_object_meta_info(key)
        return ObjectMetadata(
            bucket_name=bucket,
            object_key=key,
            size=meta["size"],
            etag=meta["ETag"],
            content_type=meta["contentType"],
            last_modified=meta["lastModified"].isoformat(),
        )
    elif provider == "cos":
        client = get_cos_client()
        resp = client.get_object(bucket, key)
        meta = resp.get_properties()
        return ObjectMetadata(
            bucket_name=bucket,
            object_key=key,
            size=meta["ContentLength"],
            etag=meta.get("ETag", ""),
            content_type=meta.get("ContentType", ""),
            last_modified=meta.get("LastModified", ""),
        )
    else:
        raise ValueError(f"Unknown provider {provider}")


def list_objects_prefix(**kwargs):
    """
    List objects under a bucket/prefix, optionally paginated.
    Provider via PROVIDER env var.
    Required kwargs:
      bucket_name
      prefix: folder-like prefix (can be empty string for root)
      max_keys: optional max per page (default 1000)
      continuation_token: optional token for pagination
    Returns ListPrefixResponse.
    """
    provider = os.getenv("PROVIDER")
    bucket = kwargs["bucket_name"]
    prefix = kwargs.get("prefix", "")
    max_keys = kwargs.get("max_keys", 1000)
    continuation_token = kwargs.get("continuation_token")

    if provider == "s3":
        client = get_s3_client()
        response = client.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix,
            MaxKeys=max_keys,
            ContinuationToken=continuation_token,
        )
        contents = [
            ObjectMetadata(
                bucket_name=bucket,
                object_key=obj["Key"],
                size=obj.get("Size", 0),
                etag=obj.get("ETag", "").strip('"'),
                content_type=obj.get("ContentType", ""),
                last_modified=obj.get("LastModified", "").isoformat(),
            )
            for obj in response.get("Contents", [])
        ]
        return ListPrefixResponse(
            bucket_name=bucket,
            prefix=prefix,
            continuation_token=response.get("NextContinuationToken"),
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
            ObjectMetadata(
                bucket_name=bucket,
                object_key=blob.name,
                size=blob.size,
                etag=blob.etag.strip('"'),
                content_type=blob.content_type,
                last_modified=blob.updated.isoformat(),
            )
            for blob in blobs
        ]
        # GCS uses page_token for continuation
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
            ObjectMetadata(
                bucket_name=bucket,
                object_key=blob.name,
                size=blob.size,
                etag=blob.properties.etag,
                content_type=blob.properties.content_type,
                last_modified=blob.properties.last_modified.isoformat(),
            )
            for blob in blobs
        ]
        return ListPrefixResponse(bucket_name=bucket, prefix=prefix, contents=contents)
    elif provider == "b2":
        client = get_b2_client()
        bucket_id = client.get_bucket_id(bucket)
        # B2 listing uses delimiters and pagination via startFileName
        resp = client.list_file_names(bucket_id, prefix=prefix, max_file_count=max_keys)
        contents = [
            ObjectMetadata(
                bucket_name=bucket,
                object_key=f["fileName"],
                size=f["size"],
                etag=f["sha1"],
                content_type=f["contentType"],
                last_modified=f["uploadTimestamp"].isoformat(),
            )
            for f in resp.get("files", [])
        ]
        return ListPrefixResponse(
            bucket_name=bucket,
            prefix=prefix,
            continuation_token=resp.get("nextFileName"),
            contents=contents,
        )
    elif provider == "oss":
        client = get_oss_client()
        resp = client.list_objects(
            prefix=prefix, max_keys=max_keys, marker=continuation_token
        )
        contents = [
            ObjectMetadata(
                bucket_name=bucket,
                object_key=obj.key,
                size=obj.size,
                etag=obj.etag,
                content_type=obj.type,
                last_modified=obj.last_modified.isoformat(),
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
            ObjectMetadata(
                bucket_name=bucket,
                object_key=obj["Key"],
                size=obj["Size"],
                etag=obj.get("ETag", ""),
                content_type=obj.get("ContentType", ""),
                last_modified=obj.get("LastModified", ""),
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
