from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def invoice_summary(payload, config=None):
    config = config or {}
    client = DocumentIntelligenceClient(config["endpoint"], AzureKeyCredential(config["api_key"]))
    summary = client.get_document_model("prebuilt-invoice").model_id if hasattr(client, "get_document_model") else "prebuilt-invoice"
    return {"summary": f"Invoice summary generated for {summary}", "invoice_count": len((payload.get('invoices') or []))}
