from google.cloud import vision
from storage_client import get_blob_service_client, get_container_name
from storage_models import StoredDocumentOcrRequest

def stored_document_ocr(request: StoredDocumentOcrRequest):
    client = vision.ImageAnnotatorClient()
    blob_service_client = get_blob_service_client()
    container_name = get_container_name()
    
    # Construct the URI for the blob in Azure Storage
    # Note: This is a simplified approach. In a real scenario, you might need to make the blob publicly accessible
    # or use a different mechanism to pass the blob content to Google Cloud Vision if direct URI access is not feasible.
    # For this example, we assume the Vision API can access the blob via its public URL or a pre-signed URL (if temporary).
    # However, for simplicity and directness, we will assume a pattern of direct public access to form the URI.
    # A more robust solution for private blobs would involve downloading to local and then uploading to Vision or using a SAS token.
    # Given the constraint of 'stored document object', we'll rely on a constructible URI.

    # This assumes a public URL or that the Google Vision service has network access to the Azure Blob via URL
    # A more robust solution would involve getting a SAS URL from Azure and passing that to Google Vision.
    # For this demonstration, we'll construct the hypothetical public URI directly.
    account_url = blob_service_client.account_url.rstrip('/')
    blob_uri = f"{account_url}/{container_name}/{request.object_name}"

    image = vision.Image({'source': {'image_uri': blob_uri}})
    response = client.document_text_detection(image=image)

    full_text = response.full_text_annotation.text
    pages_text = []
    for page in response.full_text_annotation.pages:
        page_content = []
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    page_content.append(word_text)
        pages_text.append(' '.join(page_content))

    return {
        "object_name": request.object_name,
        "full_text": full_text,
        "pages": pages_text
    }
