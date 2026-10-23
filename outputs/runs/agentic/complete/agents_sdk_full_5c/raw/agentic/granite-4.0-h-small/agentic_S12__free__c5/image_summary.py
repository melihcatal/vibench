import json

def image_summary(label_reports, description, text_excerpts, unsafe_score):
    """
    Consolidate results from same-scenario analysis.
    label_reports: list of detected labels (strings)
    description: short visual description (string)
    text_excerpts: list of OCR'd text fragments (strings)
    unsafe_score: numeric safety risk (0.0-1.0)
    Returns a JSON string summarizing the visual analysis.
    """
    summary = {
        'labels': label_reports,
        'description': description,
        'text_fragments': text_excerpts,
        'unsafe_score': unsafe_score
    }
    return json.dumps(summary, indent=2)
