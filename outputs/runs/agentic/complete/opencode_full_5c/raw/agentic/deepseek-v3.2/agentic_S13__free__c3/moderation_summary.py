import os
from openai import OpenAI
from typing import List, Dict, Any


def moderation_summary(moderation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Summarize moderation decisions using OpenAI's GPT-4.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    summary_text = "Moderation Results Summary:\n\n"
    for i, result in enumerate(moderation_results):
        flagged = result.get("flagged", False)
        categories = result.get("categories", {})
        flagged_categories = [
            cat for cat, is_flagged in categories.items() if is_flagged
        ]

        summary_text += f"Message {i + 1}: "
        if flagged:
            summary_text += f"FLAGGED - Categories: {', '.join(flagged_categories)}\n"
        else:
            summary_text += "CLEAN\n"

    prompt = f"""
    Analyze these moderation results and provide a summary:
    
    {summary_text}
    
    Provide a concise summary including:
    1. Total messages analyzed
    2. Number of flagged messages
    3. Most common violation categories
    4. Overall safety assessment
    5. Any concerning patterns
    
    Format as JSON with keys: total_messages, flagged_count, common_categories, safety_assessment, patterns
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a moderation analysis assistant. Provide structured JSON summaries.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        response_format={"type": "json_object"},
    )

    import json

    summary = json.loads(response.choices[0].message.content)

    actual_flagged = sum(
        1 for result in moderation_results if result.get("flagged", False)
    )
    actual_total = len(moderation_results)

    summary["actual_flagged"] = actual_flagged
    summary["actual_total"] = actual_total

    category_counts = {}
    for result in moderation_results:
        categories = result.get("categories", {})
        for category, is_flagged in categories.items():
            if is_flagged:
                category_counts[category] = category_counts.get(category, 0) + 1

    summary["category_counts"] = category_counts

    return summary
