from datetime import datetime, timedelta
from typing import List, Dict
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from security_models import RotationStatus

def rotation_summary(payload, config=None) -> Dict[str, List[RotationStatus]]:
    config = config or {}
    vault_url = config['vault_url']
    
    with DefaultAzureCredential() as credential:
        client = SecretClient(vault_url=vault_url, credential=credential)
        
        summary_list: List[RotationStatus] = []
        
        # Define a rotation interval for demonstration purposes (e.g., 90 days)
        rotation_interval_days = payload.get('rotation_interval_days', 90)
        
        for secret_properties in client.list_properties_of_secrets():
            secret_id = secret_properties.name
            last_rotated = secret_properties.updated_on or secret_properties.created_on
            
            status = "unknown"
            next_rotation_due = None

            if last_rotated:
                next_rotation_due = last_rotated + timedelta(days=rotation_interval_days)
                if datetime.now(last_rotated.tzinfo) > next_rotation_due:
                    status = "overdue_for_rotation"
                else:
                    status = "rotation_up_to_date"
            else:
                status = "no_rotation_info"

            summary_list.append(
                RotationStatus(
                    secret_id=secret_id,
                    last_rotated=last_rotated.isoformat() if last_rotated else None,
                    next_rotation_due=next_rotation_due.isoformat() if next_rotation_due else None,
                    status=status
                )
            )
            
        return {"rotation_summary": [s.__dict__ for s in summary_list]}
