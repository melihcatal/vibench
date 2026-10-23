from document_client import get_language_client
from azure.ai.textanalytics import TextDocumentInput
from typing import List, Dict, Any

def extract_fields_from_text(text: str, project_name: str, deployment_name: str) -> List[Dict[str, Any]]:
    client = get_language_client()

    document = [TextDocumentInput(id="1", text=text)]

    # For custom text extraction, you would typically use a custom trained model.
    # The example below assumes a custom deployment that can extract entities.
    # Replace with your actual project and deployment names.
    response = client.begin_analyze_actions(
        document,
        actions=[
            {"kind": "CustomEntityRecognition", "document_languange": "en", "project_name": project_name, "deployment_name": deployment_name}
        ]
    ).result()

    extracted_fields = []
    for result in response:
        if result.is_error:
            print(f"...Is an error with code '{result.code}' and message '{result.message}'")
        else:
            for entity in result.entities:
                extracted_fields.append({"text": entity.text, "category": entity.category, "confidence_score": entity.confidence_score, "offset": entity.offset, "length": entity.length})
    
    return extracted_fields
