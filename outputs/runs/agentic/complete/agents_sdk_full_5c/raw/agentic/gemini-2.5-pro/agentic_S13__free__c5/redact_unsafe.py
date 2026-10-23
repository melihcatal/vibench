from safety_client import get_google_perspective_client
from safety_models import RedactionRequest, RedactedText

def redact_unsafe(request: RedactionRequest) -> RedactedText:
    """
    Identifies and redacts unsafe text spans using the Google Perspective API.

    This function identifies spans that are likely toxic and replaces them
    with a placeholder.

    Args:
        request: A RedactionRequest object containing the text.

    Returns:
        A RedactedText object with the original text, redacted text, and
        the locations of unsafe spans.
    """
    client = get_google_perspective_client()
    
    analyze_request = {
        'comment': {'text': request.text},
        'requestedAttributes': {'TOXICITY': {'spanScoring': True}},
        'languages': ['en']
    }

    response = client.comments().analyze(body=analyze_request).execute()
    
    spans_to_redact = []
    if 'TOXICITY' in response['attributeScores']:
        toxicity_score = response['attributeScores']['TOXICITY']
        if 'spanScores' in toxicity_score:
            for span_score in toxicity_score['spanScores']:
                # Redact if the span score is high
                if span_score['score']['value'] > 0.8:
                    begin = span_score['span']['begin']
                    end = span_score['span']['end']
                    spans_to_redact.append((begin, end))

    text_list = list(request.text)
    for start, end in spans_to_redact:
        length = end - start
        text_list[start:end] = ['*'] * length

    redacted_text = "".join(text_list)
    
    return RedactedText(
        original_text=request.text,
        redacted_text=redacted_text,
        unsafe_spans=spans_to_redact
    )
