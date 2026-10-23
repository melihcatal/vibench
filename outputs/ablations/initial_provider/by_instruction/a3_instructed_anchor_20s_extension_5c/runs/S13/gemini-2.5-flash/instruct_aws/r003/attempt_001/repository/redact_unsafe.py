from safety_client import get_aws_comprehend_client
from safety_models import RedactionRequest, RedactionResponse
from typing import List, Dict, Any

def redact_unsafe(request: RedactionRequest) -> RedactionResponse:
    client = get_aws_comprehend_client()
    redacted_text = list(request.text)
    unsafe_spans: List[Dict[str, Any]] = []

    # Using AWS Comprehend's detect_pii_entities as a proxy for identifying 'unsafe' spans
    # for redaction, to demonstrate AWS integration. In a real content safety system,
    # a dedicated moderation API or custom model would provide these spans.
    try:
        response = client.detect_pii_entities(Text=request.text, LanguageCode='en')
        for entity in response.get('Entities', []):
            begin_offset = entity.get('BeginOffset')
            end_offset = entity.get('EndOffset')
            entity_type = entity.get('Type')
            score = entity.get('Score')

            if begin_offset is not None and end_offset is not None:
                # Redact the identified span
                for i in range(begin_offset, end_offset):
                    redacted_text[i] = '*'

                unsafe_spans.append({
                    "start": begin_offset,
                    "end": end_offset,
                    "type": entity_type,
                    "score": score
                })
    except Exception as e:
        print(f"Error with AWS Comprehend detect_pii_entities: {e}")

    # Simple keyword redaction for demonstration if AWS PII doesn't cover specific 'unsafe' terms
    # For instance, if 'badword' is considered unsafe and needs redaction.
    # This part is a simple placeholder to show a redaction mechanism.
    bad_words = ["badword", "unsafe_term"]
    original_text = request.text
    for word in bad_words:
        start_idx = 0
        while True:
            start_idx = original_text.lower().find(word, start_idx)
            if start_idx == -1:
                break
            end_idx = start_idx + len(word)
            for i in range(start_idx, end_idx):
                redacted_text[i] = '*'
            unsafe_spans.append({
                "start": start_idx,
                "end": end_idx,
                "type": "CustomFlaggedTerm",
                "score": 1.0
            })
            start_idx = end_idx

    return RedactionResponse(redacted_text="".join(redacted_text), unsafe_spans=unsafe_spans)
