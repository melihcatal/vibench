import os
import json
import boto3
from typing import Dict, Any
from uuid import uuid4

def image_asset_archive(image_path: str, analyses: Dict[str, Any], bucket: str, prefix: str = &quot;image_analysis/&quot;) -&gt; str:
    s3_client = boto3.client(
        &#x27;s3&#x27;,
        aws_access_key_id=os.getenv(&#x27;AWS_ACCESS_KEY_ID&#x27;),
        aws_secret_access_key=os.getenv(&#x27;AWS_SECRET_ACCESS_KEY&#x27;),
        region_name=os.getenv(&#x27;AWS_DEFAULT_REGION&#x27;, &#x27;us-east-1&#x27;)
    )
    artifacts = {
        &#x27;image_path&#x27;: image_path,
        &#x27;analyses&#x27;: analyses,
        &#x27;timestamp&#x27;: os.getenv(&#x27;TIMESTAMP&#x27;, &#x27;&#x27;)
    }
    obj_key = f&quot;{{prefix}}{{uuid4()}}.json&quot;
    s3_client.put_object(
        Bucket=bucket,
        Key=obj_key,
        Body=json.dumps(artifacts, indent=2)
    )
    return f&quot;s3://{{bucket}}/{{obj_key}}&quot;