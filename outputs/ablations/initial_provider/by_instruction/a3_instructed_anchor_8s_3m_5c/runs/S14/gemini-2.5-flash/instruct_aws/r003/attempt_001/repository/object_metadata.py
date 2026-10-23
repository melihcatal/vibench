from storage_client import get_s3_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse

def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    s3_client = get_s3_client()
    response = s3_client.head_object(
        Bucket=request.bucket_name,
        Key=request.object_key
    )
    # Filter out boto-specific keys that are not part of the actual metadata
    metadata = {
        k: v for k, v in response.items()
        if k not in ['ResponseMetadata', 'DeleteMarker', 'AcceptRanges', 'LastModified', 'ContentLength',
                      'ETag', 'MissingMeta', 'VersionId', 'CacheControl', 'ContentDisposition',
                      'ContentEncoding', 'ContentLanguage', 'ContentType', 'Expires', 'ServerSideEncryption',
                      'Metadata', 'SSECustomerAlgorithm', 'SSECustomerKeyMD5', 'SSEKMSKeyId',
                      'BucketKeyEnabled', 'StorageClass', 'RequestCharged', 'ReplicationStatus',
                      'TagCount', 'ObjectLockMode', 'ObjectLockRetainUntilDate', 'ObjectLockLegalHoldStatus']
    }
    # S3 user-defined metadata is under the 'Metadata' key
    if 'Metadata' in response:
        metadata.update(response['Metadata'])

    return ObjectMetadataResponse(metadata=metadata)
