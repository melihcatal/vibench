import os
from typing import List, Dict, Any
from safety_client import SafetyClient


def moderation_summary(moderation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Summarize moderation decisions.

    Args:
        moderation_results: List of moderation results from moderate_batch

    Returns:
        Summary statistics and insights
    """
    client = SafetyClient.get_client()

    # Use Anthropic Claude to generate summary
    import anthropic

    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    if not anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY not configured")

    claude_client = anthropic.Anthropic(api_key=anthropic_api_key)

    # Prepare data for summary
    total_messages = len(moderation_results)
    flagged_messages = sum(1 for r in moderation_results if r.get("flagged", False))
    flagged_percentage = (
        (flagged_messages / total_messages * 100) if total_messages > 0 else 0
    )

    # Count categories
    category_counts = {}
    for result in moderation_results:
        if "categories" in result:
            for category in result["categories"]:
                category_counts[category] = category_counts.get(category, 0) + 1
        elif "decisions" in result:
            for category, flagged in result["decisions"].items():
                if flagged:
                    category_counts[category] = category_counts.get(category, 0) + 1

    # Create prompt for Claude
    prompt = f"""You are a content moderation analyst. Summarize the following moderation results:

Total messages analyzed: {total_messages}
Flagged messages: {flagged_messages} ({flagged_percentage:.1f}%)
Category breakdown: {category_counts}

Provide a concise summary including:
1. Overall safety assessment
2. Most common violation types
3. Recommendations for policy adjustments if needed
4. Any patterns or trends observed

Keep the summary professional and actionable."""

    try:
        response = claude_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=500,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}],
        )

        summary_text = response.content[0].text

    except Exception as e:
        summary_text = f"Error generating summary: {str(e)}"

    # Calculate statistics
    avg_scores = {}
    if moderation_results and "scores" in moderation_results[0]:
        # Initialize score accumulators
        score_sums = {}
        score_counts = {}

        for result in moderation_results:
            if "scores" in result:
                for category, score in result["scores"].items():
                    score_sums[category] = score_sums.get(category, 0) + score
                    score_counts[category] = score_counts.get(category, 0) + 1

        for category in score_sums:
            if score_counts[category] > 0:
                avg_scores[category] = score_sums[category] / score_counts[category]

    return {
        "total_messages": total_messages,
        "flagged_messages": flagged_messages,
        "flagged_percentage": flagged_percentage,
        "category_counts": category_counts,
        "average_scores": avg_scores,
        "summary": summary_text,
        "provider": "anthropic",
        "model": "claude-3-opus-20240229",
    }
