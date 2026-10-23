import json
from pathlib import Path
from typing import List, Dict

# Placeholder aggregation of KMS CloudWatch metrics via API client

# Simulated function that calls a managed KMS usage reporting endpoint
# For demonstration we read a JSON file that would be produced by a cloud metric collector

def load_usage_snapshot() -> List[Dict]:
    # In production this would be an API call like
    # client.get_metric_statistics(..., Namespace='AWS/KMS', MetricName='KMSRequests')
    # Here we read a static file for illustration
    snapshot_path = Path(__file__).with_name('usage_snapshot.json')
    if snapshot_path.is_file():
        return json.loads(snapshot_path.read_text())
    return []


def key_usage_summary() -> None:
    """Print a concise summary of key usage and crypto events."""
    snapshots = load_usage_snapshot()
    total_requests = sum(s.get('count', 0) for s in snapshots)
    key_ids = sorted({s.get('key_id') for s in snapshots})
    print(f"Total KMS requests in snapshot: {total_requests}")
    print(f"Distinct keys accessed: {len(key_ids)}")
    for k in key_ids:
        print(f"  - {k}: {sum(s.get('count',0) for s in snapshots if s.get('key_id')==k)} requests")
