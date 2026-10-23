from google.cloud import documentai_v1 as documentai
from typing import List, Dict, Any

def extract_fields_from_document(project_id: str, location: str, processor_id: str, document_content: bytes) -> Dict[str, Any]:
    client = documentai.DocumentProcessorServiceClient()
    name = client.processor_path(project_id, location, processor_id)

    document = documentai.RawDocument(content=document_content, mime_type='application/pdf')

    request = documentai.ProcessRequest(name=name, raw_document=document)

    result = client.process_document(request=request)
    
    # The Document object contains the extracted entities (fields)
    # The exact structure depends on the processor type and training
    return result.document._pb
