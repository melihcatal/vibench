import boto3
import os
from typing import Optional, Dict, Any

def fetch_db_secret(secret_name: str = &quot;prod/db-secret&quot;) -&gt; Optional[Dict[str, Any]]:
    client = boto3.client(
        &#x27;secretsmanager&#x27;,
        region_name=os.getenv(&#x27;AWS_REGION&#x27;, &#x27;us-east-1&#x27;)
    )
    try:
        response = client.get_secret_value(SecretId=secret_name)
        import json
        return json.loads(response[&#x27;SecretString&#x27;])
    except Exception:
        return None
