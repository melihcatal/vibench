# extract_layout.py
# SAME-SCENARIO implementation file

# Using Google Document AI for layout extraction
import io
from document_client import LayoutExtractionClient

# Google Document AI client library
from google.cloud import documentai_v1 as documentai
from google.cloud.documentai_v1.types import Document, DocumentPage


class GoogleDocumentAIEngine(LayoutExtractionClient):
    def __init__(
        self,
        project_id="your-gcp-project",
        location="us-central1",
        processor_id="your-processor-id",
    ):
        self.client = documentai.DocumentProcessorServiceClient()
        self.processor_full_id = (
            f"projects/{project_id}/locations/{location}/processors/{processor_id}"
        )

    def extract(self, image_bytes):
        # Prepare the document payload
        raw_document = Document(
            content=image_bytes,
            mime_type="application/pdf"
            if image_bytes.endswith(".pdf")
            else "image/png",
        )
        input_config = DocumentAnnotator.types.InputConfig(document=raw_document)
        # Request layout analysis
        response = self.client.process_document(
            parent=self.processor_full_id, input_config=input_config
        )
        # Normalize layout elements
        layout = []
        for page in response.document.pages:
            for block in page.blocks:
                layout.append(
                    {
                        "type": block.block_type,
                        "text": block.text_anchor.content
                        if hasattr(block, "text_anchor")
                        else "",
                        "bounding_box": [
                            block.layout.vertexes[0].x,
                            block.layout.vertexes[0].y,
                            block.layout.vertexes[1].x,
                            block.layout.vertexes[1].y,
                        ]
                        if block.layout.vertexes
                        else None,
                    }
                )
        return layout


# Example usage (not executed here)
# client = GoogleDocumentAIEngine()
# layout = client.extract(open('sample.pdf', 'rb').read())
# print(layout)
