import os

class DocumentClient:
    """
    Provides local configuration and client helper utilities for OCR and Layout Extraction.
    """

    def __init__(self, api_key: str = None, endpoint: str = None):
        """
        Initializes the DocumentClient with API key and endpoint.
        These can be provided as arguments or will be read from environment variables.
        """
        self.api_key = api_key or os.getenv("DOCUMENT_OCR_API_KEY")
        self.endpoint = endpoint or os.getenv("DOCUMENT_OCR_ENDPOINT")

        if not self.api_key:
            raise ValueError("API Key not provided and DOCUMENT_OCR_API_KEY environment variable not set.")
        if not self.endpoint:
            raise ValueError("Endpoint not provided and DOCUMENT_OCR_ENDPOINT environment variable not set.")

    def _send_request(self, method: str, path: str, data: dict = None, files: dict = None) -> dict:
        """
        Internal helper to send requests to the OCR/Layout Extraction service.
        This is a placeholder and would be replaced with actual HTTP client code (e.g., using requests library).
        """
        print(f"Sending {method} request to {self.endpoint}{path}")
        print(f"Headers: {{'Authorization': f'Bearer {self.api_key}'}}")
        if data:
            print(f"Data: {data}")
        if files:
            print(f"Files: {files.keys()}")
        
        # In a real implementation, this would make an actual API call
        # and handle responses, errors, etc.
        # For now, it returns a mock response.
        return {"status": "success", "message": "Mock response from OCR service"}

    def extract_ocr_text(self, image_bytes: bytes) -> dict:
        """
        Extracts plain text from a scanned document image using the OCR service.
        """
        # This is a placeholder for actual OCR text extraction logic
        # In a real scenario, image_bytes would be sent to the OCR service
        # and the extracted text would be part of the response.
        print("Performing OCR text extraction...")
        files = {"document": ("image.png", image_bytes, "image/png")}
        return self._send_request("POST", "/ocr/text", files=files)

    def extract_layout(self, document_bytes: bytes, layout_type: str = "blocks") -> dict:
        """
        Extracts layout elements (blocks, lines, tables) from a document using the layout extraction service.
        """
        # This is a placeholder for actual layout extraction logic
        print(f"Performing layout extraction for type: {layout_type}...")
        files = {"document": ("document.pdf", document_bytes, "application/pdf")}
        data = {"layout_type": layout_type}
        return self._send_request("POST", "/layout/extract", data=data, files=files)

