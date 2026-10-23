import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.hlp.model import PromptTemplate
from document_models import OcrResult

def extract_fields(ocr_result: OcrResult) -> dict:
    """Extract structured fields from a form‑like OCR document using a foundation model.
    Returns a dictionary mapping field names to their extracted values.
    """
    client = APIClient(
        api_key=os.getenv('WATSONX_API_KEY'),
        url=os.getenv('WATSONX_URL'),
        project_id=os.getenv('WATSONX_PROJECT_ID')
    )
    # Example prompt – in practice use the exact field list required by your workflow
    prompt = PromptTemplate(
        "You have a scanned form. Extract the following fields and their values as JSON:\n\n- Full Name\n- Email\n- Phone\n- Address\n- Date of Birth\n\nReturn the result as a single JSON object."
    )
    response = client.generate_content(
        model_id='google-gecko',  # replace with the actual model ID from your catalog
        prompt=prompt,
        parameters={'max_new_tokens': 200, 'temperature': 0.0},
        content=ocr_result.full_text
    )
    import json
    return json.loads(response.generations[0].text)
