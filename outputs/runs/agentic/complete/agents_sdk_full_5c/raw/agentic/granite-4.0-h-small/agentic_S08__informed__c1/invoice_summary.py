import os
import json
from ibm_watsonx_ai.nlp import GraniteModel
from document_models import InvoiceDocument
from document_client import GenericClient
from watsonx_ai import WatsonX
from watsonx_ai.identity import Credentials


def invoice_summary(file_path: str):
    # 1️⃣ Extract structured data (using Mindee as example same‑scenario extractor)
    mindee_client = GenericClient()   # placeholder – in practice use extract_invoice_fields from extract_invoice_fields.py
    invoice: InvoiceDocument = extract_invoice_fields(file_path)  # <-- function defined in other file
    # 2️⃣ Build a prompt for summarisation
    prompt = f"Create a concise two‑sentence summary of the invoice below. Include vendor name, total amount, and top three line items.\nInvoice data:\n{json.dumps(invoice, indent=2)}"
    # 3️⃣ Call Granite LLM via watsonx.ai SDK
    creds = Credentials(
        apikey=os.getenv('WATSONX_API_KEY'),
        url=os.getenv('WATSONX_URL')
    )
    watsonx_client = WatsonX(identity=creds)
    model = GraniteModel(project_id=os.getenv('WATSONX_PROJECT_ID'))
    response = model.chat(
        messages=[{'role': 'user', 'content': prompt}],
        model_version='ibm/granite-13b-chat-v2'
    )
    summary = response.choices[0].message.content
    return summary
