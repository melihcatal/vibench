import os
from typing import Dict, Any
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import Model

watsonx_api_key = os.getenv("WATSONX_API_KEY")
watsonx_project_id = os.getenv("WATSONX_PROJECT_ID")
watsonx_url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

client = APIClient(api_key=watsonx_api_key, url=watsonx_url)


def summarize_invoice(invoice_data: Dict[str, Any]) -> str:
    model_id = "ibm/granite-13b-chat-v2"
    model = Model(
        model_id=model_id,
        params={"decoding_method": "greedy"},
        credentials={"apikey": watsonx_api_key, "url": watsonx_url},
        project_id=watsonx_project_id,
    )
    
    prompt = f"Summarize the following invoice data in a concise paragraph:\n{invoice_data}"
    
    response = model.generate_text(prompt=prompt)
    return response