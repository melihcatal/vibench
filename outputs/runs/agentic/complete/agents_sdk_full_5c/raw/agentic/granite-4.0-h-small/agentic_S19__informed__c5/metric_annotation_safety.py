import os
from observability_client import MonitoringClient
from observability_models import MetricQueryRequest
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

def metric_annotation_safety(metric_query: MetricQueryRequest):
    """Check free‑text metric labels or annotations for unsafe text using Azure AI Content Safety.

    Requires env vars: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
    """
    # ----- Azure Content Safety client -----
    endpoint = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
    key = os.getenv('AZURE_CONTENT_SAFETY_KEY')
    if not endpoint or not key:
        raise RuntimeError('Azure Content Safety credentials not configured')
    content_safety = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    # ----- Retrieve recent metric data (labels) -----
    client = MonitoringClient()
    query = metric_query.to_dict()
    raw_points = client.fetch_time_series(query)
    # Assume the metric has a label called 'annotation' containing free text
    annotations = []
    for point in raw_points:
        for sample in point.points:
            val = sample.value.string_value
            if val:
                annotations.append(val)

    # ----- Moderation ----- 
    if not annotations:
        return {'status': 'no_annotations', 'details': []}
    response = content_safety.analyze_text(content='\n'.join(annotations), content_type='text/plain')
    unsafe = [
        {'text': ann, 'flags': result.flags, 'category_scores': result.category_scores}
        for ann, result in zip(annotations, response.results)
        if result.flagged
    ]
    return {'status': 'checked', 'unsafe_items': unsafe}
