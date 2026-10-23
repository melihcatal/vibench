import boto3
from datetime import datetime, timedelta
from typing import List, Dict

class KeyUsageSummary:
    def __init__(self):
        self.client = boto3.client('kms')

    def get_key_usage(self, key_id: str, days: int = 7) -> List[Dict]:
        start_time = datetime.utcnow() - timedelta(days=days)
        response = self.client.get_key_rotation_status(KeyId=key_id)
        
        # Fetch usage metrics from AWS CloudTrail or KMS logs (simplified)
        usage = self.client.list_key_policies(KeyId=key_id)
        
        return [
            {
                "key_id": key_id,
                "rotation_enabled": response.get("KeyRotationEnabled", False),
                "usage_policy": usage.get("PolicyNames", []),
                "period_start": start_time.isoformat(),
                "period_end": datetime.utcnow().isoformat()
            }
        ]