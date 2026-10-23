import os
from google.cloud import documentai_v1 as documentai
from storage_models import OCRRequest, OCRResponse


def run_ocr_on_stored_document(
    file_content,
    mime_type,
    project_id=None,
    processor_id=None,
    location=None,
):
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
    processor_id = processor_id or os.environ.get(
        "DOCUMENT_AI_PROCESSOR_ID", "ocr-processor"
    )
    location = location or os.environ.get("DOCUMENT_AI_LOCATION", "us")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is required")
    request = OCRRequest(
        file_content=file_content,
        mime_type=mime_type,
        project_id=project_id,
        processor_id=processor_id,
        location=location,
    )
    client_options = {"api_endpoint": f"{request.location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)
    name = client.processor_path(
        request.project_id, request.location, request.processor_id
    )
    import base64

    document = {
        "content": base64.b64encode(request.file_content).decode("utf-8"),
        "mime_type": request.mime_type,
    }
    response = client.process_document(name=name, document=document)
    document_text = response.document.text
    pages_data = []
    for page in response.document.pages:
        page_text = ""
        for block in page.blocks:
            block_text = ""
            for paragraph in block.paragraphs:
                paragraph_text = ""
                for word in paragraph.words:
                    word_text = ""
                    for symbol in word.symbols:
                        word_text += symbol.text
                    paragraph_text += word_text + " "
                block_text += paragraph_text
            page_text += block_text
        pages_data.append({"text": page_text.strip(), "confidence": page.confidence})
    overall_confidence = (
        sum(p["confidence"] for p in pages_data) / len(pages_data)
        if pages_data
        else 0.0
    )
    return OCRResponse(
        text=document_text,
        pages=pages_data,
        confidence=overall_confidence,
    )
