import json
from typing import List, Dict, Any
import os
from mistralai import Mistral

def moderation_summary(decisions: List[Dict[str, Any]]) -> str:
    api_key = os.getenv(&quot;MISTRAL_API_KEY&quot;)
    client = Mistral(api_key=api_key)
    messages = [
        {&quot;role&quot;: &quot;system&quot;, &quot;content&quot;: &quot;You are a helpful assistant. Provide a concise summary of the moderation decisions, highlighting any patterns, risky content, and overall safety assessment.&quot;},
        {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: json.dumps(decisions, indent=2)}
    ]
    chat_response = client.chat(
        model=&quot;mistral-large-latest&quot;,
        messages=messages
    )
    return chat_response.choices[0].message.content