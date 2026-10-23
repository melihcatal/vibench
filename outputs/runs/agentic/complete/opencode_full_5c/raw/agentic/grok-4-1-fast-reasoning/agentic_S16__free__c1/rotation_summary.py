import boto3
import os
from typing import Dict, Any

def rotation_summary(secret_name: str = &quot;prod/rotatable-secret&quot;) -&gt; str:
    client = boto3.client(
        &#x27;secretsmanager&#x27;,
        region_name=os.getenv(&#x27;AWS_REGION&#x27;, &#x27;us-east-1&#x27;)
    )
    try:
        response = client.describe_secret(SecretId=secret_name)
        rot_config = response.get(&#x27;RotationConfiguration&#x27;, {})
        enabled = bool(rot_config.get(&#x27;RotationLambdaARN&#x27;))
        arn = rot_config.get(&#x27;RotationLambdaARN&#x27;, &#x27;N/A&#x27;)
        rules_str = str(rot_config.get(&#x27;RotationRules&#x27;, {}))
        summary = f&quot;Rotation Status for {{secret_name}}: enabled={{enabled}}, Lambda={{arn}}, Rules={{rules_str}}&quot;
        return summary
    except Exception as e:
        return f&quot;Error fetching rotation summary: {{str(e)}}&quot;
