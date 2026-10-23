from storage_client import StorageClient
from storage_models import UploadObjectRequest, UploadObjectResponse
from google.cloud import storage # Provider-identifying signal

def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    client = StorageClient().get_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)

    blob.upload_from_string(request.data, content_type=request.content_type)

    # Make the object publicly accessible. This is optional and depends on use case.
    # blob.make_public()

    return UploadObjectResponse(
        bucket_name=request.bucket_name,
        object_name=request.object_name,
        size=len(request.data),
        public_url=blob.public_url if blob.public_url else None # Check if public_url exists
    )
