
from google.cloud import translate_v3 as translate
import os
from document_client import GoogleTranslateManager
from document_models import ExpenseRecord

def translate_invoice_notes(expense_record: ExpenseRecord, target_language_code: str = "en") -> str:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation API.
    """
    project_id = os.getenv("GCP_PROJECT_ID")
    location = os.getenv("GCP_LOCATION", "global") # Global endpoint for Translation API

    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")
    if not expense_record.notes:
        return "" # No notes to translate

    translate_manager = GoogleTranslateManager(project_id, location)
    client = translate_manager.get_translate_client()
    parent = translate_manager.get_parent()

    contents = [expense_record.notes]

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": contents,
            "target_language_code": target_language_code,
            # Optional: source_language_code can be specified if known
            # "source_language_code": "fr",
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text

    return translated_text

if __name__ == '__main__':
    # Example usage
    expense_with_french_notes = ExpenseRecord(
        document_type="invoice",
        vendor_name="La Boulangerie",
        transaction_date="2023-10-20",
        total_amount=25.50,
        notes="Merci pour votre achat. Voici le reçu.",
        line_items=[]
    )

    # Ensure GCP_PROJECT_ID is set as an environment variable
    # translated = translate_invoice_notes(expense_with_french_notes, "en")
    # print("Original Notes:", expense_with_french_notes.notes)
    # print("Translated Notes (en):", translated)

    expense_no_notes = ExpenseRecord(
        document_type="invoice",
        vendor_name="No Notes Inc.",
        transaction_date="2023-10-21",
        total_amount=50.00,
        notes=None,
        line_items=[]
    )
    # translated_no_notes = translate_invoice_notes(expense_no_notes, "es")
    # print("Translated Notes (no notes):", translated_no_notes)
    pass
