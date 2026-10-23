from google.cloud import vision


def normalize_labels(labels):
    return [label.description for label in labels]


def normalize_description(description):
    return description


def normalize_text(text_annotations):
    return [annotation.description for annotation in text_annotations]


def normalize_safety(safety):
    return {
        "adult": safety.adult,
        "medical": safety.medical,
        "violence": safety.violence,
        "racy": safety.racy,
    }
