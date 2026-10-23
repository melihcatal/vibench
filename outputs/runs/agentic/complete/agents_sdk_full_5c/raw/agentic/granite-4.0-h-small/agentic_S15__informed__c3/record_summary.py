import json
from record_fetch import fetch_user_profile
from record_safety import check_text_safety
from record_translate import translate_text
from record_export import archive_snapshot

# ------------------------------------------------------------
# record_summary.py
# ------------------------------------------------------------
# This file uses the full stack: fetch → safety → translation → export snapshot

def summarize_document(doc_id):
    # 1️⃣ Fetch the raw record
    raw = fetch_user_profile(doc_id)
    if not raw:
        raise ValueError(f"Document {doc_id} not found")
    
    # 2️⃣ Verify that the free‑form text fields are safe
    safe_text = check_text_safety(raw.get('description', ''))
    # Replace original with the cleaned version (or keep both)
    raw['description'] = safe_text
    
    # 3️⃣ Translate a user‑facing field (e.g., name) to Spanish
    translated_name = translate_text(raw.get('name', ''), target='es')
    raw['name_es'] = translated_name
    
    # 4️⃣ Export a snapshot of the processed record to object storage
    archive_snapshot(raw, f"snapshot_{doc_id}.json")
    
    # 5️⃣ Return a compact summary for downstream services
    summary = {
        'id': raw['_id'],
        'name_en': raw['name'],
        'name_es': translated_name,
        'category': raw.get('category'),
        'safe': True
    }
    return summary

if __name__ == "__main__":
    # Run with a concrete doc_id for demonstration
    doc_id = 'user-123'
    summary = summarize_document(doc_id)
    print('Summary:
', json.dumps(summary, indent=2))
