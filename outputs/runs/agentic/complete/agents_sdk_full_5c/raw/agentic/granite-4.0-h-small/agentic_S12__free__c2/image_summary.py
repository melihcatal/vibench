import json

def image_summary(label_scores, description, ocr_texts, safety_info):
    '''Combine outputs from analysis steps into a concise summary.
    label_scores: list of detected labels with confidence (list of dicts)
    description: short visual caption (str)
    ocr_texts: list of extracted text blocks (list of dicts with 'text')
    safety_info: dict with unsafe flag & confidence
    '''
    summary = {
        'labels': label_scores,
        'description': description,
        'extracted_text': [txt['text'] for txt in ocr_texts],
        'safety': {
            'unsafe': safety_info.get('unsafe', False),
            'confidence': safety_info.get('confidence', 0.0)
        }
    }
    return json.dumps(summary, indent=2)
