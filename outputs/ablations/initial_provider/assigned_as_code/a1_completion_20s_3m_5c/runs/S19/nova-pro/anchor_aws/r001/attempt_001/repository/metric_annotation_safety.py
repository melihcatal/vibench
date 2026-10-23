import re


def metric_annotation_safety(payload):
    annotation = payload['annotation']
    if re.search(r'[a-zA-Z0-9]{4,}', annotation):
        return {'safe': True}
    return {'safe': False}