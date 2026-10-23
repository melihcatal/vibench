import os
from typing import List, Dict, Any
import openai


def moderation_summary(moderation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Summarize moderation decisions using OpenAI's GPT-4.
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    flagged_count = sum(
        1 for result in moderation_results if result.get("flagged", False)
    )
    total_count = len(moderation_results)

    category_counts = {}
    for result in moderation_results:
        categories = result.get("categories", {})
        for category, flagged in categories.items():
            if flagged:
                category_counts[category] = category_counts.get(category, 0) + 1

    summary_prompt = f"""
    Analyze these moderation results and provide a summary:
    - Total texts: {total_count}
    - Flagged texts: {flagged_count}
    - Category breakdown: {category_counts}
    
    Provide a concise summary of the moderation findings.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a content moderation analyst. Summarize moderation results clearly and professionally.",
            },
            {"role": "user", "content": summary_prompt},
        ],
        temperature=0.3,
        max_tokens=200,
    )

    summary_text = response.choices[0].message.content.strip()

    return {
        "summary": summary_text,
        "statistics": {
            "total_texts": total_count,
            "flagged_texts": flagged_count,
            "flag_rate": flagged_count / total_count if total_count > 0 else 0,
            "category_counts": category_counts,
            "most_common_violation": max(category_counts.items(), key=lambda x: x[1])[0]
            if category_counts
            else None,
        },
        "recommendations": generate_recommendations(
            flagged_count, total_count, category_counts
        ),
    }


def generate_recommendations(
    flagged_count: int, total_count: int, category_counts: Dict[str, int]
) -> List[str]:
    """Generate recommendations based on moderation statistics."""
    recommendations = []

    flag_rate = flagged_count / total_count if total_count > 0 else 0

    if flag_rate > 0.3:
        recommendations.append(
            "High flag rate detected. Consider reviewing community guidelines."
        )
    elif flag_rate > 0.1:
        recommendations.append("Moderate flag rate. Monitor for trends.")

    if category_counts.get("violence", 0) > 0:
        recommendations.append(
            "Violence content detected. Consider implementing stricter filters."
        )

    if category_counts.get("hate", 0) > 0:
        recommendations.append("Hate speech detected. Review hate speech policies.")

    if category_counts.get("sexual_minors", 0) > 0:
        recommendations.append(
            "Child safety concerns detected. Immediate action recommended."
        )

    return recommendations
