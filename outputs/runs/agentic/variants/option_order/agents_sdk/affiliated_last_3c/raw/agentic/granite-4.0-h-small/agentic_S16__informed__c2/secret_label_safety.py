import os
from perspective import PerspectiveClient
from security_client import get_project_id

def secret_label_safety(secret_value: str, label_key='labels') -> bool:
    # Assume secret_value is JSON with a 'labels' dict
    import json
    data = json.loads(secret_value)
    labels = data.get(label_key, {})
    client = PerspectiveClient(api_key=os.getenv('PERSPECTIVE_API_KEY'))
    toxicity = client.analyze(text=' '.join(labels.values()), attributes={'TOXICITY': {}})
    return toxicity['attributeScores']['TOXICITY']['summaryScore']['value'] < 0.5
