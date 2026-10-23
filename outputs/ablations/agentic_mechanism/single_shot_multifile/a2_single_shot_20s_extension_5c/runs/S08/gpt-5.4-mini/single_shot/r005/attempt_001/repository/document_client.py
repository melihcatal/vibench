import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI

from document_models import DocumentExtractionRequest, ExtractionResult


@dataclass(frozen=True)
class DocumentSettings:
    openai_api_key: Optional[str]
    openai_model: str


def load_document_settings() -> DocumentSettings:
    return DocumentSettings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
    )


class StructuredDocumentClient:
    def __init__(self, settings: DocumentSettings):
        self.settings = settings
        self.client = OpenAI(api_key=settings.openai_api_key)

    def extract(self, request: DocumentExtractionRequest) -> ExtractionResult:
        response = self.client.responses.create(
            model=request.model or self.settings.openai_model,
            input=[
                {
                    "role": "system",
                    "content": "You are a structured document extraction engine. Return only valid JSON."
                },
                {
                    "role": "user",
                    "content": f"Task: {request.task_name}\nSchema: {request.schema_name}\nInstructions: {request.instructions}\nDocument:\n{request.document_text}"
                },
            ],
            text={"format": {"type": "json_object"}},
        )
        return ExtractionResult.from_openai_response(response)
