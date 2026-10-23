# [HELPER] document_client.py

import os
from typing import Any, Dict, Optional

# --------------------------------------------------------------------------
# Provider configuration
# --------------------------------------------------------------------------
# Each supported provider has a minimal client wrapper.  Credentials are read
# from environment variables defined in the "Requirements" section of the spec.
# --------------------------------------------------------------------------


class DocumentClient:
    """Thin wrapper around a concrete OCR / layout / table / key‑value provider."""

    _SUPPORTED_SERVICES = {
        # OCR / Layout providers (same‑scenario)
        "mindee": "mindee",
        "azure_document_intelligence": "azure-ai-documentintelligence",
        "alibabacloud_ocr_api": "alibabacloud_ocr_api",
        "google_document_ai": "google-cloud-documentai",
        # ... add others as needed
        # Later‑step service names (kept here for completeness)
        "azure_ai_translator": "azure-ai-translation-text",
        "amazon_translate": "boto3",
        "alibaba_machine_translation": "alibabacloud_alimt",
        "deepl": "deepl",
        "google_cloud_translation": "google-cloud-translate",
    }

    def __init__(self, service: str) -> None:
        if service not in self._SUPPORTED_SERVICES:
            raise ValueError(
                f"Unsupported service '{service}'. Choose from {list(self._SUPPORTED_SERVICES)}"
            )
        self.service = service
        # Import the real SDK only when needed; this keeps the helper lightweight.
        if service.startswith("mindee"):
            from mindee import MindeeClient

            self._client = MindeeClient(api_key=os.getenv("MINDEE_API_KEY"))
        elif service == "azure_document_intelligence":
            from azure.ai.documentintelligence import DocumentIntelligenceClient
            from azure.identity import DefaultAzureCredential

            self._client = DocumentIntelligenceClient(
                endpoint=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"),
                credential=DefaultAzureCredential(),
            )
        elif service == "alibabacloud_ocr_api":
            import alibabacloud_ocr_api  # type: ignore

            self._client = alibabacloud_ocr_api.ocr_client(
                access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
                access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
            )
        elif service == "google_document_ai":
            from google.cloud import documentai

            self._client = documentai.DocumentProcessorServiceClient()
            # Expect GOOGLE_APPLICATION_CREDENTIALS env var for auth
        else:
            raise NotImplementedError(
                f"Client stub for service {service} not implemented."
            )

    # ----------------------------------------------------------------------
    # Common convenience methods (all translate internally to the concrete SDK)
    # ----------------------------------------------------------------------

    def ocr(self, image_path: str) -> Dict[str, Any]:
        """Run OCR on an image and return a dict matching the generic response format."""
        if self.service.startswith("mindee"):
            resp = self._client.process(image_path)
            # Normalize to a generic layout: {text, fields}
            return {
                "text": resp.text,
                "fields": resp.fields,
            }
        elif self.service == "azure_document_intelligence":
            poller = self._client.begin_analyze_layout(image_path)
            result = poller.result()
            # Return Azure’s "readResults" directly (layout focus)
            return {"readResults": result.read_results}
        elif self.service == "alibabacloud_ocr_api":
            resp = self._client.ocr(image_path)
            return {
                "text": resp.get("text", ""),
                "fields": resp.get("fields", {}),
            }
        elif self.service == "google_document_ai":
            # Form parsing, layout, or generic document processing can be selected here.
            # For simplicity we call the generic processor.
            name = f"projects/{os.getenv('GOOGLE_PROJECT_ID')}/locations/global/processors/{os.getenv('GOOGLE_DOCUMENT_AI_PROCESSOR_ID')}/process"
            response = self._client.process_document(
                name=name,
                input_document={
                    "mime_type": "image/jpeg",
                    "content": open(image_path, "rb").read(),
                },
            )
            # Simplify to a generic dict: {"text":..., "fields":..., "tables":...}
            doc = response.document
            return {
                "text": " ".join([t.text for t in doc.tokens]),
                "fields": {
                    n: v.text
                    for n, v in doc.entities.items()
                    if v.type_ in {"KEY", "VALUE"}
                },
                "tables": [t for t in doc.tables if t.rows > 0],  # placeholder
            }
        else:
            raise NotImplementedError(f"OCR method not implemented for {self.service}")

    def analyze_form(self, image_path: str) -> Dict[str, Any]:
        """Key‑value extraction using generic provider (Google Document AI as example)."""
        # Reuse the generic Google Document AI implementation shown above.
        return self.ocr(
            image_path
        )  # placeholder; replace with real form logic as needed

    def translate(self, source_text: str, target_lang: str) -> str:
        """Generic translation wrapper (Azure Translator used as example)."""
        if self.service == "azure_ai_translator":
            from azure.ai.translation.text import TextTranslationClient
            from azure.identity import DefaultAzureCredential

            client = TextTranslationClient(
                endpoint=os.getenv("AZURE_TRANSLATOR_ENDPOINT"),
                credential=DefaultAzureCredential(),
            )
            result = client.translate_text(
                source_text, from_language="en", to_language=target_lang
            )
            return result.translations[0].translated_text
        # Add other translation providers similarly...
        raise NotImplementedError(f"Translation not implemented for {self.service}")

    def detect_safety(self, text: str) -> Dict[str, Any]:
        """Safety/content moderation wrapper (Azure Content Safety example)."""
        if self.service == "azure_ai_content_safety":
            from azure.ai.contentsafety import ContentSafetyClient
            from azure.identity import DefaultAzureCredential

            client = ContentSafetyClient(
                endpoint=os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
                credential=DefaultAzureCredential(),
            )
            result = client.analyze_content(
                text=text,
                moderation_categories=["violence", "self_harm", "harassment", "hate"],
            )
            return {"labels": result.labels, "scores": result.scores}
        # Add other providers…
        raise NotImplementedError(
            f"Safety detection not implemented for {self.service}"
        )

    def embed(self, text: str) -> list[float]:
        """Embedding wrapper (Gemini embeddings example)."""
        if self.service == "google_gemini":
            from google.generativeai import GeminiEmbeddingClient

            client = GeminiEmbeddingClient()
            embedding = client.embed_content(text)
            return embedding.embedding
        # Add other providers…
        raise NotImplementedError(f"Embedding not implemented for {self.service}")


# --------------------------------------------------------------------------
# Utility helpers
# --------------------------------------------------------------------------


def load_env_vars(required: list[str]) -> None:
    """Verify required environment variables are set."""
    missing = [v for v in required if not os.getenv(v)]
    if missing:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing)}"
        )


# Example usage (uncomment to test locally)
# if __name__ == "__main__":
#     load_env_vars(["MINDEE_API_KEY"])  # adjust per selected provider
#     client = DocumentClient(service="mindee")
#     print(client.ocr("sample.jpg"))
