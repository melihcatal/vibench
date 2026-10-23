from google.cloud import documentai_v1 as documentai
from document_models import DocumentRequest, TextExtractionResponse
from typing import List, Dict, Any

def extract_layout_from_document(project_id: str, location: str, processor_id: str, document_content: bytes) -> Dict[str, Any]:
    client = documentai.DocumentProcessorServiceClient()
    
    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    name = client.processor_path(project_id, location, processor_id)

    document = documentai.RawDocument(content=document_content, mime_type='application/pdf')

    request = documentai.ProcessRequest(name=name, raw_document=document)

    result = client.process_document(request=request)
    
    # For layout extraction, the Document object contains the layout information
    return result.document._pb
