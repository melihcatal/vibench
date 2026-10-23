def check_text_safety(text):
    # Placeholder for text safety check logic
    return 'Unsafe' if 'unsafe' in text.lower() else 'Safe'

def visual_safety_text(labels):
    return [check_text_safety(label) for label in labels]
