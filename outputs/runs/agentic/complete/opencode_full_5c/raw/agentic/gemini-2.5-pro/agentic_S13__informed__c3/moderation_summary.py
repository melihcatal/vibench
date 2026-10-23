import os
from openai import OpenAI
from typing import List, Dict


def summarize_moderation_decisions(decisions: List[Dict]) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt_lines = ["Summarize the following content moderation decisions:"]
    for decision in decisions:
        line = f"- Text: '{decision.get('text', 'N/A')}', Is Safe: {decision.get('is_safe', 'N/A')}, Categories: {decision.get('categories', 'N/A')}"
        prompt_lines.append(line)

    prompt = "\n".join(prompt_lines)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a content moderation analyst providing concise summaries.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred with OpenAI API: {e}")
        return "Could not generate summary due to an API error."
