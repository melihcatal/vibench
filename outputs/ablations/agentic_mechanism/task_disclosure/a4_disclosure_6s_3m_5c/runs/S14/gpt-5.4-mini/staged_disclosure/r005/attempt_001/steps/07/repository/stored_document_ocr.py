import os
from typing import Any, Dict, Optional

from google.cloud import vision


def run_stored_document_ocr(
    gcs_source_uri: str,
    mime_type: str = "application/pdf",
    language_hints: Optional[list[str]] = None,
) -> Dict[str, Any]:
    client = vision.ImageAnnotatorClient()
    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)
    gcs_source = vision.GcsSource(uri=gcs_source_uri)
    input_config = vision.InputConfig(
        gcs_source=gcs_source,
        mime_type=mime_type,
    )
    pages = []
    if language_hints:
        pages = []
    context = vision.ImageContext(language_hints=language_hints or [])
    request = vision.AsyncAnnotateFileRequest(
        features=[feature],
        input_config=input_config,
        image_context=context,
    )
    operation = client.async_annotate_file(requests=[request])
    result = operation.result(timeout=int(os.getenv("GOOGLE_VISION_OCR_TIMEOUT", "600")))

    texts = []
    for response in result.responses:
        if response.full_text_annotation and response.full_text_annotation.text:
            texts.append(response.full_text_annotation.text)

    return {
        "source_uri": gcs_source_uri,
        "mime_type": mime_type,
        "text": "\n".join(texts),
        "page_count": len(texts),
    }


def main() -> None:
    gcs_source_uri = os.environ["GCS_SOURCE_URI"]
    output = run_stored_document_ocr(gcs_source_uri=gcs_source_uri)
    print(output["text"])


if __name__ == "__main__":
    main()
