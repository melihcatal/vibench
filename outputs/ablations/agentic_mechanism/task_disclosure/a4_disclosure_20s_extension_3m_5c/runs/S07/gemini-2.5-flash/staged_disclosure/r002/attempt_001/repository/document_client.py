
class DocumentClient:
    def __init__(self, config=None):
        self.config = config if config else {}

    def ocr_document(self, document_path: str):
        """
        Performs OCR on a document.
        :param document_path: Path to the document.
        :return: OCR results.
        """
        print(f"Performing OCR on {document_path} with config: {self.config}")
        # Placeholder for OCR logic
        return {"text_content": "Extracted text from document.", "confidence": 0.95}

    def extract_layout(self, document_path: str):
        """
        Extracts layout information from a document.
        :param document_path: Path to the document.
        :return: Layout extraction results.
        """
        print(f"Extracting layout from {document_path} with config: {self.config}")
        # Placeholder for layout extraction logic
        return {"tables": [], "paragraphs": [], "figures": []}

    def process_document(self, document_path: str):
        """
        Combines OCR and layout extraction for a comprehensive document processing.
        :param document_path: Path to the document.
        :return: Combined OCR and layout extraction results.
        """
        ocr_results = self.ocr_document(document_path)
        layout_results = self.extract_layout(document_path)
        return {"ocr": ocr_results, "layout": layout_results}
