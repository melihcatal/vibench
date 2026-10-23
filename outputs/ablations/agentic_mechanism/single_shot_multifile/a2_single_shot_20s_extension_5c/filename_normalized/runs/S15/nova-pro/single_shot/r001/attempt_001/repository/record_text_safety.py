from safety_checker import check_safety

def record_text_safety(document):
    text = document.get('text', '')
    return check_safety(text)