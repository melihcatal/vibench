import os
from typing import Optional
from alibabacloud_ocr_api20210707.models import RecognizeTextRequest
from document_client import create_ocr_client, encode_image_to_base64
from document_models import DocumentTextResult, OcrLine, OcrWord


def extract_text_from_image(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> DocumentTextResult:
    client = create_ocr_client()
    image_base64 = encode_image_to_base64(image_path, image_bytes)

    request = RecognizeTextRequest(body=image_base64)
    response = client.recognize_text(request)

    body = response.body
    raw_text = ""
    lines = []
    overall_confidence = 1.0

    if hasattr(body, "data") and body.data:
        data = body.data
        if isinstance(data, dict):
            raw_text = data.get("content", data.get("text", ""))
            page_lines = data.get("lines", [])
            for line_data in page_lines:
                words = []
                for word_data in line_data.get("words", []):
                    word = OcrWord(
                        text=word_data.get("text", ""),
                        confidence=word_data.get("confidence", 0.0),
                    )
                    words.append(word)
                if words:
                    lines.append(OcrLine(words=words))
            overall_confidence = data.get("confidence", 1.0)
        elif isinstance(data, str):
            raw_text = data
            lines = [OcrLine(words=[OcrWord(text=data, confidence=1.0)])]

    if not lines and raw_text:
        lines = [OcrLine(words=[OcrWord(text=raw_text, confidence=overall_confidence)])]

    return DocumentTextResult(
        raw_text=raw_text,
        lines=lines,
        confidence=overall_confidence,
        page_count=1,
    )


if __name__ == "__main__":
    image_file = os.environ.get("DOCUMENT_IMAGE_PATH")
    if image_file:
        result = extract_text_from_image(image_path=image_file)
        print(result.raw_text)
