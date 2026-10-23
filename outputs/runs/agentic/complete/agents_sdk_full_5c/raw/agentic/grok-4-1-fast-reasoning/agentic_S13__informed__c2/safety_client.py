import os
from typing import Dict

def load_safety_config() -&gt; Dict[str, str]:
    return {
        &quot;endpoint&quot;: os.getenv(&quot;AZURE_CONTENT_SAFETY_ENDPOINT&quot;),
        &quot;key&quot;: os.getenv(&quot;AZURE_CONTENT_SAFETY_KEY&quot;)
    }