import os
from openai import OpenAI
from typing import List, Dict, Any


def moderation_summary(moderation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Summarize moderation decisions using OpenAI's GPT-4.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Prepare data for summarization
    summary_data = []
    for i, result in enumerate(moderation_results):
        flagged_categories = []
        for category, flagged in result.get("categories", {}).items():
            if flagged:
                flagged_categories.append(category)

        summary_data.append(
            {
                "index": i,
                "flagged": result.get("flagged", False),
                "flagged_categories": flagged_categories,
                "category_scores": result.get("category_scores", {}),
            }
        )

    # Create prompt for summarization
    prompt = f"""Summarize the following moderation results:

{summary_data}

Provide a concise summary including:
1. Total number of items moderated
2. Number of items flagged
3. Most common violation categories
4. Overall safety assessment
5. Recommendations for next steps

Return the summary as a JSON object with these fields:
- "total_items": integer
- "flagged_items": integer
- "flag_rate": float (percentage)
- "common_categories": list of objects with "category" and "count"
- "overall_assessment": string
- "recommendations": list of strings
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a content moderation analyst. Summarize moderation results concisely.",
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )

    summary = eval(response.choices[0].message.content)

    # Add raw statistics
    total_items = len(moderation_results)
    flagged_items = sum(
        1 for result in moderation_results if result.get("flagged", False)
    )

    # Calculate category frequencies
    category_counts = {}
    for result in moderation_results:
        for category, flagged in result.get("categories", {}).items():
            if flagged:
                category_counts[category] = category_counts.get(category, 0) + 1

    # Sort categories by frequency
    sorted_categories = sorted(
        category_counts.items(), key=lambda x: x[1], reverse=True
    )

    summary.update(
        {
            "raw_statistics": {
                "total_items": total_items,
                "flagged_items": flagged_items,
                "flag_rate": flagged_items / total_items if total_items > 0 else 0,
                "category_frequencies": dict(sorted_categories),
            }
        }
    )

    return summary
