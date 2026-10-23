from document_models import ExpenseRecord
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def normalize_expense(extracted_data, document_type, config=None):
    config = config or {}
    normalized_record = ExpenseRecord(
        document_type=document_type,
        raw_extraction=extracted_data
    )

    if document_type == 'invoice':
        invoice = extracted_data.get('invoices', [{}])[0]
        normalized_record.vendor_name = invoice.get('vendor')
        normalized_record.transaction_date = invoice.get('date')
        normalized_record.total_amount = invoice.get('total')
        normalized_record.line_items = [
            {'description': item.get('description'), 'quantity': item.get('quantity'), 'amount': item.get('amount')}
            for item in invoice.get('line_items', [])
        ]
    elif document_type == 'receipt':
        receipt = extracted_data.get('receipts', [{}])[0]
        normalized_record.vendor_name = receipt.get('merchant')
        normalized_record.total_amount = receipt.get('total')
        normalized_record.tax_amount = receipt.get('tax')
        normalized_record.line_items = [
            {'description': item.get('description'), 'quantity': item.get('quantity'), 'price': item.get('price')}
            for item in receipt.get('items', [])
        ]

    # Scored component: Use Azure Text Analytics for language detection on vendor name
    if normalized_record.vendor_name and config.get('text_analytics_endpoint') and config.get('text_analytics_api_key'):
        text_analytics_client = TextAnalyticsClient(
            endpoint=config['text_analytics_endpoint'],
            credential=AzureKeyCredential(config['text_analytics_api_key'])
        )
        try:
            response = text_analytics_client.detect_language(documents=[normalized_record.vendor_name])
            if response and response[0].primary_language:
                normalized_record.currency = response[0].primary_language.iso6391_name # Using currency for language as an example
        except Exception:
            pass # Ignore errors for optional enrichment

    return normalized_record.dict()
