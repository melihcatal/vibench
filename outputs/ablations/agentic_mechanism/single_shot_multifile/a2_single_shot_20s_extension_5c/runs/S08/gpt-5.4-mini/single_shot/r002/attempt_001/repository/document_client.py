import json
import os
from dataclasses import dataclass
from typing import Any, Dict

from openai import OpenAI

from document_models import DocumentExtractionRequest


@dataclass
class StructuredDocumentClient:
    api_key_env: str = "OPENAI_API_KEY"

    def _client(self) -> OpenAI:
        api_key = os.getenv(self.api_key_env)
        if not api_key:
            raise RuntimeError(f"Missing required environment variable: {self.api_key_env}")
        return OpenAI(api_key=api_key)

    def extract_with_openai(self, *, model: str, request: DocumentExtractionRequest, schema_name: str) -> Dict[str, Any]:
        prompt = request.to_prompt(schema_name=schema_name)
        response = self._client().responses.create(model=model, input=prompt)
        text = response.output_text
        try:
            data = json.loads(text)
        except Exception:
            data = {"raw_text": text}
        data["provider"] = "openai"
        data["model"] = model
        data["document_type"] = request.document_type
        return data


def get_extraction_client() -> StructuredDocumentClient:
    return StructuredDocumentClient()
