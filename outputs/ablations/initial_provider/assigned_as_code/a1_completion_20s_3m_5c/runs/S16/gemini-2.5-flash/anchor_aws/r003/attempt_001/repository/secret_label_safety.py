import boto3
import re

def secret_label_safety(payload, config=None):
    config = config or {}
    comprehend_client = boto3.client("comprehend", region_name=config.get("region"))

    unsafe_keywords = ["password", "key", "secret", "token", "cred"]
    unsafe_labels_found = False
    unsafe_notes_found = False
    details = {"unsafe_label_matches": [], "unsafe_note_matches": []}

    for label_key, label_value in payload.get("labels", {}).items():
        for keyword in unsafe_keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', label_key, re.IGNORECASE) or \
               re.search(r'\b' + re.escape(keyword) + r'\b', label_value, re.IGNORECASE):
                unsafe_labels_found = True
                details["unsafe_label_matches"].append({"key": label_key, "value": label_value, "keyword": keyword})

    notes = payload.get("notes")
    if notes:
        for keyword in unsafe_keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', notes, re.IGNORECASE):
                unsafe_notes_found = True
                details["unsafe_note_matches"].append({"notes_snippet": notes, "keyword": keyword})
                break # Only need to find one keyword to mark notes as unsafe
        
        # Advanced check using Comprehend for PII in notes
        try:
            pii_response = comprehend_client.detect_pii_entities(Text=notes, LanguageCode='en')
            if pii_response['Entities']:
                unsafe_notes_found = True
                details["pii_in_notes"] = pii_response['Entities']
        except comprehend_client.exceptions.TextSizeLimitExceededException:
            details["pii_in_notes_warning"] = "Notes too long for PII detection."


    return {
        "secret_id": payload["secret_id"],
        "unsafe_labels_found": unsafe_labels_found,
        "unsafe_notes_found": unsafe_notes_found,
        "details": details,
    }
