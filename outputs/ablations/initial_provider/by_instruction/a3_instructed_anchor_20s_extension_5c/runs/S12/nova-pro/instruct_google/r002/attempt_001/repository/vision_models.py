def normalize_labels(labels):
    return [label.description for label in labels]

def normalize_description(description):
    return ' '.join(description)

def normalize_text(text):
    return text

def normalize_safety(safety):
    return safety.__dict__