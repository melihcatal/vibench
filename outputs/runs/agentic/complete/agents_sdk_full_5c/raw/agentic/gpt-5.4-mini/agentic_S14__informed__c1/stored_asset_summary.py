from typing import Optional

from openai import OpenAI

from stored_document_ocr import run_stored_document_ocr
from storage_models import SummaryResult

SUMMARY_MODEL = "gpt-4o-mini"


def summarize_stored_asset(
    object_name: str,
    bucket_name: Optional[str] = None,
    project_id: Optional[str] = None,
    location: str = "us",
    processor_id: Optional[str] = None,
) -> SummaryResult:
    ocr_result = run_stored_document_ocr(
        object_name=object_name,
        bucket_name=bucket_name,
        project_id=project_id,
        location=location,
        processor_id=processor_id,
    )
    client = OpenAI()
    response = client.chat.completions.create(
        model=SUMMARY_MODEL,
        messages=[
            {"role": "system", "content": "Summarize extracted document content concisely."},
            {"role": "user", "content": ocr_result.text},
        ],
    )
    return SummaryResult(summary=response.choices[0].message.content or "", source_text=ocr_result.text)
