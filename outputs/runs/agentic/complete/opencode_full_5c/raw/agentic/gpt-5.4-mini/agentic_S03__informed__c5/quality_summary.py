import os
from typing import Dict, List

from openai import OpenAI


def summarize_quality_issues(issues: List[str]) -> Dict[str, str]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize translation quality issues concisely.",
            },
            {"role": "user", "content": "\n".join(issues)},
        ],
    )
    return {"provider": "OpenAI", "summary": response.choices[0].message.content}
