import json

def image_summary(viz_result):
    """Create a concise JSON-safe summary of the visual analysis.",
    # Expected structure of viz_result: dict with keys from each analysis step
    summary = {
        'labels': viz_result.get('labels', []),
        'description': viz_result.get('description', ''),
        'text': viz_result.get('text', []),
        'safety_rating': viz_result.get('safety_rating', '')
    }
    return json.dumps(summary)
