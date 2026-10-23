import os
from typing import List, Dict, Any
from openai import OpenAI


def moderation_summary(moderation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Summarize moderation decisions using OpenAI's GPT model.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    summary_data = []
    for result in moderation_results:
        summary_data.append(
            {
                "text": result.get("text", result.get("message", "")),
                "flagged": result.get("flagged", False),
                "categories": result.get("flagged_categories", []),
                "decision": result.get(
                    "decision", "reject" if result.get("flagged", False) else "allow"
                ),
            }
        )

    prompt = f"""
    Summarize the following moderation decisions:
    
    {summary_data}
    
    Provide a summary including:
    1. Total number of items moderated
    2. Number of flagged items
    3. Most common violation categories
    4. Overall moderation rate
    5. Any notable patterns or trends
    
    Format the response as a JSON object with these fields.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a moderation analytics assistant. Summarize moderation data and return JSON.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        response_format={"type": "json_object"},
    )

    summary = response.choices[0].message.content

    import json

    try:
        summary_dict = json.loads(summary)
    except json.JSONDecodeError:
        summary_dict = {"summary": summary}

    total_items = len(summary_data)
    flagged_items = sum(1 for item in summary_data if item["flagged"])

    summary_dict.update(
        {
            "total_items": total_items,
            "flagged_items": flagged_items,
            "moderation_rate": flagged_items / total_items if total_items > 0 else 0,
        }
    )

    return summary_dict
