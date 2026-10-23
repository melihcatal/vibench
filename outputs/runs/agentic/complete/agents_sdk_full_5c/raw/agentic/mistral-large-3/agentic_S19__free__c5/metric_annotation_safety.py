from google.cloud import monitoring_v3
from google.api import label_descriptor_pb2
from observability_client import get_monitoring_client
import re

def check_annotation_safety(project_id: str, metric_type: str) -> dict:
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"
    
    metric_name = f"{project_name}/metricDescriptors/{metric_type}"
    metric = client.get_metric_descriptor(name=metric_name)
    
    unsafe_pattern = re.compile(r"[<>'\"&%$#@!*]+")
    
    results = {}
    for label in metric.labels:
        label_value = label.description
        if unsafe_pattern.search(label_value):
            results[label.key] = {
                "status": "unsafe",
                "description": label_value
            }
        else:
            results[label.key] = {
                "status": "safe",
                "description": label_value
            }
    
    return results