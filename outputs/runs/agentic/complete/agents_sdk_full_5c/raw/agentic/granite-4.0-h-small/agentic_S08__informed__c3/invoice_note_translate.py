import requests
from document_models import ExpenseRecord

DEEPL_API_KEY = os.getenv("DEEPL_AUTH_KEY")

def translate_invoice_notes(record: ExpenseRecord, target_lang: str = "en") -> ExpenseRecord:
    if not record.raw_data.get("invoice_notes"):
        return record
    payload = {
        "text": record.raw_data["invoice_notes"],
        "target_lang": target_lang
    }
    headers = {"Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"}
    resp = requests.post("https://api.deepl.com/v2/translate", data=payload, headers=headers)
    resp.raise_for_status()
    translation = resp.json()["translations"][0]["text"]
    # Store both original and translated version
    record.raw_data["invoice_notes_translated"] = translation
    return record
