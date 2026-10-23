from security_client import SecretManagementClient
from security_models import SecretProperties
from datetime import datetime

def rotation_summary(config: dict = None) -> dict:
    config = config or {}
    client = SecretManagementClient(vault_url=config.get('vault_url'))
    
    secrets_summary = []
    for secret_properties in client.list_properties_of_secrets():
        properties = SecretProperties(
            id=secret_properties.id,
            name=secret_properties.name,
            enabled=secret_properties.enabled,
            expires_on=secret_properties.expires_on.timestamp() if secret_properties.expires_on else None,
            created_on=secret_properties.created_on.timestamp() if secret_properties.created_on else None,
            updated_on=secret_properties.updated_on.timestamp() if secret_properties.updated_on else None,
            tags=secret_properties.tags,
            content_type=secret_properties.content_type,
            recoverable_days=secret_properties.recoverable_days,
        )
        
        status = "Unknown"
        if properties.expires_on:
            expires_datetime = datetime.fromtimestamp(properties.expires_on)
            if expires_datetime < datetime.now():
                status = "Expired"
            elif (expires_datetime - datetime.now()).days < 30: # Example: expiring soon (within 30 days)
                status = "Expiring Soon"
            else:
                status = "Active"
        elif properties.updated_on:
             updated_datetime = datetime.fromtimestamp(properties.updated_on)
             if (datetime.now() - updated_datetime).days > 90: # Example: not updated in 90 days
                 status = "Stale (No Recent Update)"
             else:
                 status = "Active (Recently Updated)"
        else:
            status = "No Expiry/Update Info"
            
        secrets_summary.append({
            "secret_id": properties.name,
            "status": status,
            "expires_on": properties.expires_on,
            "updated_on": properties.updated_on,
            "tags": properties.tags,
        })
        
    return {"rotation_summary": secrets_summary}
