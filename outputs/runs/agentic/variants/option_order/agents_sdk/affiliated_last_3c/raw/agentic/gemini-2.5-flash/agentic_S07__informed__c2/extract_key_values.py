import os
from azure.ai.documentintelligence import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from typing import Dict, List

def extract_key_value_pairs(document_path: str) -> Dict[str, List[Dict]]:
    """
    Extracts key-value pairs from a form-like document using Azure Document Intelligence.
    Uses the 'prebuilt-document' model which can detect key-value pairs in general documents.
    """
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(document_path, "rb") as f:
        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-document", document=f.read()
        )
        result = poller.result()

    key_value_pairs = {"fields": []}
    if result.key_value_pairs:
        for kvp in result.key_value_pairs:
            key_value_pairs["fields"].append({
                "key": kvp.key.content if kvp.key else None,
                "value": kvp.value.content if kvp.value else None,
                "confidence": kvp.confidence
            })
    
    # Also include general fields detected by prebuilt-document
    if result.fields:
        for field_name, field_value in result.fields.items():
            key_value_pairs["fields"].append({
                "key": field_name,
                "value": field_value.content if field_value else None,
                "confidence": field_value.confidence if field_value else None
            })

    return key_value_pairs

if __name__ == '__main__':
    # Example usage (requires environment variables set and a test document)
    # key_values = extract_key_value_pairs("path/to/your/form.pdf")
    # for field in key_values["fields"]:
    #     print(f"Key: {field['key']}, Value: {field['value']}, Confidence: {field['confidence']}")
    pass
