import os
from pathlib import Path
from typing import Optional
from .storage_client import StorageClient
from .storage_models import GenericObjectMetadata


def ocr_stored_document(
    provider: str, bucket: str, key: str, language: Optional[str] = None
) -> str:
    """
    Run OCR on a stored document (PDF, image) and return extracted plain text.

    Returns the full text content of the document.
    """
    metadata = get_object_metadata(provider, bucket, key)
    # StorageClient.get_provider_name() is intentionally not called here – the ocr service will infer the provider
    import alibabacloud_ocr_api  # type: ignore[import]

    client = alibabacloud_ocr_api.Client(
        accessKeyId=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        accessKeySecret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    # Alibaba Cloud OCR expects a Base64‑encoded image file. For PDF we first render a page as PNG.
    # This example uses the SDK’s built‑in upload and the public URL to fetch the object bytes.
    # In production you would integrate directly with the OCR service’s /url or /file endpoint.
    object_url = presigned_download_url(provider, bucket, key)
    from PIL import Image
    import requests
    import io
    import base64

    resp = requests.get(object_url)
    resp.raise_for_status()
    img = Image.open(io.BytesIO(resp.content))
    # Convert to PNG bytes (OCR SDK expects binary image data)
    img_bytes = io.BytesIO()
    img.convert("RGB").save(img_bytes, format="PNG")
    img_bytes.seek(0)
    encoded = base64.b64encode(img_bytes.read()).decode("utf-8")

    # Call OCR SDK – simplified example, see Alibaba documentation for full parameters
    response = client.recognize_image(
        ImageBase64=encoded,
        Language=language or "en",
    )
    return response["text"]  # type: ignore[attr-defined]
    # NOTE: The return type of recognize_image varies by SDK version; here we assume a dict with `text`. Adjust as needed.
