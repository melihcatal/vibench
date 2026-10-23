import boto3
import os
from typing import Optional

def rotate_secret_version(secret_name: str = &quot;prod/rotatable-secret&quot;, version_stage: str = &quot;AWSPENDING&quot;) -&gt; Optional[str]:
    client = boto3.client(
        &#x27;secretsmanager&#x27;,
        region_name=os.getenv(&#x27;AWS_REGION&#x27;, &#x27;us-east-1&#x27;)
    )
    try:
        response = client.get_secret_value(
            SecretId=secret_name,
            VersionStage=version_stage
        )
        return response[&#x27;SecretString&#x27;]
    except Exception:
        return None
