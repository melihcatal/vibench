# Local configuration and client helper utilities for Structured Document Extraction

import os
import json

# --------------------------------------------------------------------------
# Provider-specific client initialization
#
# This module supplies a generic DocumentExtractionClient class that internally
# instantiates the SDK / HTTP client for a concrete third‑party service.  The
# provider is identified by the client factory function (e.g., `from_azure`,
# `from_google`, `from_uipath`).  Consumers import ``DocumentExtractionClient``
# from this module to keep the rest of the codebase provider‑agnostic.


class DocumentExtractionClient:
    """
    Abstract client wrapper for third‑party structured document extraction services.
    Concrete factories are defined below; callers should use `from_config()`.
    """

    def __init__(self, provider: str, credentials: dict):
        self.provider = provider
        self.credentials = credentials
        # The actual SDK client is lazily instantiated in `extract`
        self._sdk = None

    @classmethod
    def from_config(cls) -> "DocumentExtractionClient":
        """Create a client using environment variables / local config.

        Expected env variables (examples):
        - AZURE_FORM_RECOGNIZER_ENDPOINT
        - AZURE_FORM_RECOGNIZER_KEY
        - GOOGLE_DOC_AI_ENDPOINT
        - GOOGLE_DOC_AI_KEY
        - UIPATH_API_ENDPOINT
        - UIPATH_API_TOKEN
        """
        # Choose provider based on defined env vars (simple priority order)
        if os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT") and os.getenv(
            "AZURE_FORM_RECOGNIZER_KEY"
        ):
            return cls.from_azure()
        if os.getenv("GOOGLE_DOC_AI_ENDPOINT") and os.getenv("GOOGLE_DOC_AI_KEY"):
            return cls.from_google()
        if os.getenv("UIPATH_API_ENDPOINT") and os.getenv("UIPATH_API_TOKEN"):
            return cls.from_uipath()
        raise RuntimeError(
            "No supported document extraction provider credentials found in environment"
        )

    @classmethod
    def from_azure(cls) -> "DocumentExtractionClient":
        """Instantiate Azure Form Recognizer client.
        Provider identifier: Azure Form Recognizer
        """
        from azure.ai.formrecognizer import DocumentAnalysisClient

        endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
        key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
        return cls(provider="azure", credentials={"endpoint": endpoint, "key": key})

    @classmethod
    def from_google(cls) -> "DocumentExtractionClient":
        """Instantiate Google Document AI client.
        Provider identifier: Google Document AI
        """
        from google.cloud import documentai_v1 as documentai

        endpoint = os.getenv("GOOGLE_DOC_AI_ENDPOINT")
        key = os.getenv("GOOGLE_DOC_AI_KEY")
        # Construct the client; the key can be a service account JSON path
        return cls(provider="google", credentials={"endpoint": endpoint, "key": key})

    @classmethod
    def from_uipath(cls) -> "DocumentExtractionClient":
        """Instantiate UiPath Document Understanding client.
        Provider identifier: UiPath Document Understanding
        """
        from uipath_sdk import DocumentExtractionClient as UIPathClient

        endpoint = os.getenv("UIPATH_API_ENDPOINT")
        token = os.getenv("UIPATH_API_TOKEN")
        return cls(
            provider="uipath", credentials={"endpoint": endpoint, "token": token}
        )

    def extract(self, form_type: str, file_path: str) -> dict:
        """
        Perform extraction using the underlying SDK.  The method returns a plain
        dictionary with the raw fields produced by the provider.
        """
        if self._sdk is None:
            self._sdk = self._build_sdk_client()
        # The SDK client is expected to have an `analyze_document`/`extract` method
        # that accepts `form_type` and `file_path`.  We delegate and return raw JSON.
        raw_result = self._sdk.analyze_document(
            form_type=form_type, file_path=file_path
        )
        return raw_result  # type: ignore

    def _build_sdk_client(self):
        if self.provider == "azure":
            endpoint = self.credentials["endpoint"]
            key = self.credentials["key"]
            # Azure SDK expects a credential object; we simply reuse the key.
            return DocumentAnalysisClient(endpoint=endpoint, credential=key)
        elif self.provider == "google":
            # Required env: GOOGLE_APPLICATION_CREDENTIALS pointing to JSON key file
            # Simple forwarder that creates a DocumentProcessorServiceClient
            from google.cloud import documentai_v1 as documentai

            return documentai.DocumentProcessorServiceClient()
        elif self.provider == "uipath":
            endpoint = self.credentials["endpoint"]
            token = self.credentials["token"]
            # Simple auth wrapper that performs a POST request to UIPATH endpoint
            import requests

            class UIPathAdapter:
                def analyze_document(self, form_type, file_path):
                    url = f"{endpoint}/v1/extract"
                    response = requests.post(
                        url,
                        json={"formType": form_type, "filePath": file_path},
                        headers={"Authorization": f"Bearer {token}"},
                    )
                    response.raise_for_status()
                    return response.json()

            return UIPathAdapter()
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
