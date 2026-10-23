import os
from typing import List, Dict, Any
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def summarize_records(records: List[Dict[str, Any]]) -> str:
    text = "\n\n".join([str(record) for record in records])
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        temperature=0.7,
        messages=[
            {
                "role": "user",
                "content": f"Summarize the key information from these document records in a concise paragraph:\\n\\n{text}",
            }
        ],
    )
    return message.content[0].text
