import os
from bedrock import Bedrock

BEDROCK_API_KEY = os.getenv('BEDROCK_API_KEY')

bedrock_client = Bedrock(api_key=BEDROCK_API_KEY)

def summarize_invoice_fields(invoice_fields):
    prompt = f"Summarize the following invoice fields: {invoice_fields}"
    response = bedrock_client.invoke_model(
        model_id='amazon.bedrock.summarization',
        input_text=prompt
    )
    return response.get('summary', '')
