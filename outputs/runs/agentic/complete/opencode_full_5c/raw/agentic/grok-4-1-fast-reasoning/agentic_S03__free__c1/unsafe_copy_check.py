import anthropic
import os
import json
from typing import Dict, Any, List[str]

def unsafe_copy_check(text: str, lang: str) -> Dict[str, Any]:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": f"Check if this {lang} text contains unsafe content (hate speech, violence, explicit sexual, illegal activities). Respond ONLY with valid JSON: {{\"safe\": true/false, \"issues\": [\"list of issues or []\"]}}\\n\\nText: {text}"
            }
        ]
    )
    content = message.content[0].text
    return json.loads(content)
