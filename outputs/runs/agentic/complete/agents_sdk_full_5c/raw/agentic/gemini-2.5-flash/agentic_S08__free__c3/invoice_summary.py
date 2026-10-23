
from google.cloud import aiplatform
from google.protobuf import json_format
from google.auth import default
import os
from document_client import GoogleVertexAIManager
from document_models import ExpenseRecord

def summarize_invoice_fields(expense_record: ExpenseRecord) -> str:
    """
    Summarizes extracted invoice fields using Google Cloud Vertex AI (text-bison@002).
    """
    project_id = os.getenv("GCP_PROJECT_ID")
    location = os.getenv("GCP_LOCATION", "us-central1") # Vertex AI often uses us-central1 for models

    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    vertex_manager = GoogleVertexAIManager(project_id, location)
    prediction_client = vertex_manager.get_prediction_client()

    # Model ID for summarization
    # The `text-bison@002` model is often available for text generation tasks.
    # Check Vertex AI documentation for latest models and their IDs.
    model_id = "text-bison@002"
    endpoint = (
        f"projects/{project_id}/locations/{location}/publishers/google/models/{model_id}"
    )

    prompt = f"""Summarize the following expense record. Focus on the vendor, total amount, and key line items.

Vendor: {expense_record.vendor_name}
Total Amount: {expense_record.total_amount} {expense_record.currency}
Line Items:
"""
    for item in expense_record.line_items:
        prompt += f"- {item.description} (Amount: {item.amount}, Quantity: {item.quantity})
"

    prompt += "
Provide a concise summary of this expense."

    instance = aiplatform.types.Instance(prompt=prompt)
    instances = [instance.to_value()]
    parameters = aiplatform.types.Parameters(
        temperature=0.2,
        max_output_tokens=256,
        top_p=0.8,
        top_k=40
    )

    try:
        response = prediction_client.predict(
            endpoint=endpoint,
            instances=instances,
            parameters=parameters.to_value()
        )
        summary = ""
        for prediction in response.predictions:
            # Predictions come as a list of dicts, extract 'content'
            if isinstance(prediction, dict) and "content" in prediction:
                summary += prediction["content"]
            elif hasattr(prediction, 'struct_value') and 'content' in prediction.struct_value:
                 summary += prediction.struct_value['content']
            elif hasattr(prediction, 'json_format'):
                # Handle different protobuf representations if needed
                struct = json_format.ParseDict(prediction, aiplatform.gapic.types.struct_pb2.Value())
                if 'content' in struct:
                    summary += struct['content']

        return summary.strip()

    except Exception as e:
        print(f"Error summarizing invoice with Vertex AI: {e}")
        return f"Error summarizing: {e}"

if __name__ == '__main__':
    # Example usage
    expense = ExpenseRecord(
        document_type="invoice",
        vendor_name="Global Tech Solutions",
        transaction_date="2023-10-25",
        total_amount=1250.75,
        currency="USD",
        line_items=[
            {"description": "Software License", "amount": 1000.0, "quantity": 1},
            {"description": "Support Plan (1 year)", "amount": 250.75, "quantity": 1}
        ],
        notes="Annual software renewal."
    )
    # Ensure GCP_PROJECT_ID and GCP_LOCATION are set as environment variables
    # For local testing, you might need to authenticate with `gcloud auth application-default login`
    # summary = summarize_invoice_fields(expense)
    # print("Invoice Summary:", summary)
    pass
