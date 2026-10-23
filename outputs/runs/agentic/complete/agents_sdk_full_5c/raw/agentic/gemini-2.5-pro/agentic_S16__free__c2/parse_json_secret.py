import os
import json
from google.cloud import secretmanager
from security_models import ApiGatewayConfig

def parse_json_secret(secret_id: str, version_id: str = "latest") -> ApiGatewayConfig | None:
    """
    Retrieves and parses a JSON-formatted secret from Google Cloud Secret Manager.
    
    Args:
        secret_id: The ID of the secret.
        version_id: The version of the secret.
        
    Returns:
        An ApiGatewayConfig object or None if an error occurs.
    """
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        print("GCP_PROJECT_ID environment variable not set.")
        return None
        
    client = secretmanager.SecretManagerServiceClient()
    
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    
    try:
        response = client.access_secret_version(request={"name": name})
        payload = response.payload.data.decode("UTF-8")
        
        secret_data = json.loads(payload)
        
        config = ApiGatewayConfig(
            api_key=secret_data.get("api_key"),
            service_url=secret_data.get("service_url"),
            timeout=secret_data.get("timeout", 60)
        )
        return config
        
    except Exception as e:
        print(f"Error accessing secret {secret_id}: {e}")
        return None
