from azure.ai.documentintelligence import AnalyzeDocumentRequest

from document_client import create_client
from document_models import DocumentInput, OCRResult


def extract_text(content_bytes: bytes, mime_type: str = "image/png") -> OCRResult:
    client = create_client()
    poller = client.begin_analyze_document(
        model_id="prebuilt-read",
        analyze_request=AnalyzeDocumentRequest(bytes_source=content_bytes),
        content_type=mime_type,
    )
    result = poller.result()
    lines = []
    for page in getattr(result, "pages", []) or []:
        for line in getattr(page, "lines", []) or []:
            lines.append(getattr(line, "content", ""))
    if not lines and getattr(result, "content", None):
        lines.append(result.content)
    return OCRResult(
        text="\n".join(line for line in lines if line).strip(), raw={"result": result}
    )
