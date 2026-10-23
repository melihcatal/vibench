import os
from typing import Any, Dict

# ---------- Provider credentials (environment variables) ----------
MINDEE_API_KEY = os.getenv("MINDEE_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


# ---------- Generic client helper utilities ----------
class DocumentClient:
    """Base client that selects the concrete provider at runtime.

    Supports:
    * Mindee (default, generic OCR)
    * Azure Document Intelligence
    * Google Document AI
    """

    def __init__(self, provider: str = "mindee"):
        if provider == "mindee":
            self._client = self._init_mindee()
        elif provider == "azure":
            self._client = self._init_azure()
        elif provider == "google":
            self._client = self._init_google()
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    # ---------- Mindee ----------
    def _init_mindee(self) -> Any:
        """Initialise Mindee client using environment credentials."""
        if MINDEE_API_KEY is None:
            raise RuntimeError("MINDEE_API_KEY environment variable not set")
        try:
            from mindee import MindeeClient
        except ImportError:
            raise ImportError("mindee package not installed; run `pip install mindee`")
        return MindeeClient(api_key=MINDEE_API_KEY)

    # ---------- Azure Document Intelligence ----------
    def _init_azure(self) -> Any:
        """Initialise Azure Document Intelligence client."""
        if AZURE_ENDPOINT is None or AZURE_KEY is None:
            raise RuntimeError("Azure credentials missing")
        try:
            from azure.ai.documentintelligence import DocumentIntelligenceClient
        except ImportError:
            raise ImportError(
                "azure-ai-documentintelligence not installed; run `pip install azure-ai-documentintelligence`"
            )
        return DocumentIntelligenceClient(endpoint=AZURE_ENDPOINT, credential=AZURE_KEY)

    # ---------- Google Document AI ----------
    def _init_google(self) -> Any:
        """Initialise Google Document AI client."""
        if GOOGLE_CREDENTIALS_PATH is None:
            raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS not set")
        try:
            from google.cloud import documentai
        except ImportError:
            raise ImportError(
                "google-cloud-documentai not installed; run `pip install google-cloud-documentai`"
            )
        client_options = {"credentials": GOOGLE_CREDENTIALS_PATH}
        return documentai.DocumentProcessorServiceClient(**client_options)

    # ---------- Public API ----------
    def process_document(self, image_path: str, product: str = "generic"):
        """Dispatch processing to the selected provider.

        Parameters:
            image_path: path to a local image file (jpg/png)
            product: service/product name; e.g. "generic", "layout", "invoice"
        Returns:
            Raw response from the underlying SDK (JSON‑like dict).
        """
        if self._client is None:
            raise RuntimeError("DocumentClient not initialised")

        # Minimal common interface – map product to provider‑specific call
        if isinstance(self._client, self._init_mindee.__return_type__):
            # Mindee uses a product argument on process_document
            return self._client.process_document(image_path, product=product)
        else:
            # Fallback to a generic upload (Azure / Google)
            with open(image_path, "rb") as img:
                # Generic request body
                body = {"document": img.read()}
                # Dispatch based on provider
                if provider == "azure":
                    return self._client.analyze_document(product, **body)
                elif provider == "google":
                    parent = "projects/PROJECT_ID/locations/global"
                    return self._client.process_document(parent, body=body)
                else:
                    raise NotImplementedError()

    def normalize_response(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize different provider shape into a unified dict with keys:
        * text: plain text
        * layout: list of blocks (each block includes type, bounding box, text)
        * tables: list of tables (rows/columns)
        * fields: list of {key, value} for forms
        """
        unified = {
            "text": "",
            "layout": [],
            "tables": [],
            "fields": [],
        }
        # Example normalisation for Mindee (adjust for Azure/Google as needed)
        if isinstance(self._client, self._init_mindee.__return_type__):
            unified["text"] = raw.get("text", "")
            unified["layout"] = raw.get("blocks", [])
            unified["tables"] = raw.get("tables", [])
            # Form fields are already in Mindee result
            unified["fields"] = raw.get("fields", [])
        return unified


# Example usage (run as script)
if __name__ == "__main__":
    client = DocumentClient(provider="mindee")
    raw = client.process_document("sample.jpg", product="generic")
    print(client.normalize_response(raw))
