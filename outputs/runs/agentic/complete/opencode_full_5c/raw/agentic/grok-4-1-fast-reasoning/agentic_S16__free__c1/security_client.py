import os
from typing import Optional, Dict, Any

# Local configuration helpers
AWS_REGION = os.getenv(&#x27;AWS_REGION&#x27;, &#x27;us-east-1&#x27;)
OPENAI_API_KEY = os.getenv(&#x27;OPENAI_API_KEY&#x27;)
GOOGLE_APPLICATION_CREDENTIALS = os.getenv(&#x27;GOOGLE_APPLICATION_CREDENTIALS&#x27;)

def get_aws_client_config() -&gt; Dict[str, Any]:
    return {&#x27;region_name&#x27;: AWS_REGION}

def get_openai_config() -&gt; Dict[str, str]:
    return {&#x27;api_key&#x27;: OPENAI_API_KEY}
