from mindee.parsing.common import Document
from mindee import Client, product
from document_client import MindeeClient
from document_models import KeyValuePair
from typing import List


def extract_key_values_from_mindee(
    file_content: bytes, filename: str
) -> List[KeyValuePair]:
    client = MindeeClient().client
    input_doc = client.doc_from_bytes(file_content, filename)

    # Using a generic financial document for key-value extraction as an example
    # In a real scenario, you'd pick a specific product like product.InvoiceV4 or product.ReceiptV5
    response = client.parse(product.FinancialDocumentV1, input_doc)

    key_value_pairs: List[KeyValuePair] = []
    if (
        response.document
        and response.document.inference
        and response.document.inference.prediction
    ):
        prediction = response.document.inference.prediction
        # Mindee's FinancialDocumentV1 doesn't have explicit key-value pairs in a direct list
        # We can simulate by extracting relevant fields as key-value pairs
        if (
            hasattr(prediction, "locale")
            and prediction.locale
            and prediction.locale.value
        ):
            key_value_pairs.append(
                KeyValuePair(key="Locale", value=prediction.locale.value)
            )
        if (
            hasattr(prediction, "total_amount")
            and prediction.total_amount
            and prediction.total_amount.value
        ):
            key_value_pairs.append(
                KeyValuePair(
                    key="Total Amount", value=str(prediction.total_amount.value)
                )
            )
        if hasattr(prediction, "date") and prediction.date and prediction.date.value:
            key_value_pairs.append(
                KeyValuePair(key="Date", value=prediction.date.value)
            )
        # Add more fields as needed based on the specific Mindee product used

    return key_value_pairs
