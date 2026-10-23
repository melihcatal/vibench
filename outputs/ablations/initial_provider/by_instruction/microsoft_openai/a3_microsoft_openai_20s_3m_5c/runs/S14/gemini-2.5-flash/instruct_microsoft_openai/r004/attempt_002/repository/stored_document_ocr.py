import os
import requests
import json

def run_ocr_on_stored_document(document_url: str):
    endpoint = os.getenv("AZURE_VISION_ENDPOINT")
    key = os.getenv("AZURE_VISION_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_VISION_ENDPOINT and AZURE_VISION_KEY environment variables not set.")

    # Using Azure AI Vision Read API for OCR
    ocr_url = f"{endpoint}/vision/v3.2/read/sync"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    data = {"url": document_url}

    try:
        response = requests.post(ocr_url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        extracted_text = []
        if 'analyzeResult' in result and 'readResults' in result['analyzeResult']:
            for page in result['analyzeResult']['readResults']:
                for line in page['lines']:
                    extracted_text.append(line['text'])
        return {"extracted_text": "\n".join(extracted_text), "full_response": result}
    except requests.exceptions.RequestException as e:
        return {"error": f"OCR failed: {e}", "details": response.text if response else "No response"}
