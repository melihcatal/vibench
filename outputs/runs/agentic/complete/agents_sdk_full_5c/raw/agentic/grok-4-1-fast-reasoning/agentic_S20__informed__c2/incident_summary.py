from typing import List
import os
from anthropic import Anthropic

def incident_summary(error_logs: List[str]) -> str:
    \"\"\"Summarize error-log findings for incident review.\"\"\"
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    logs_text = '\\n'.join(error_logs)
    message = client.messages.create(
        model='claude-3-haiku-20240307',
        max_tokens=500,
        temperature=0.1,
        messages=[
            {
                'role': 'user',
                'content': f'Summarize these error logs for incident review. Highlight patterns, root causes, and actions:\\n\\n{logs_text}'
            }
        ]
    )
    return message.content[0].text
