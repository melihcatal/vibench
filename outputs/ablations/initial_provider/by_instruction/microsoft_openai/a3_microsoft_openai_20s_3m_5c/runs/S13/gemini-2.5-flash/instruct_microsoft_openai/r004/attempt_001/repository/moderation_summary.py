import os
from openai import OpenAI
from safety_models import TextModerationResponse

def summarize_moderation_decisions(response: TextModerationResponse) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    if not client.api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")

    decision_text = "Moderation decisions:\n"
    if response.categories:
        for cat in response.categories:
            decision_text += f"  - Category: {cat.get('category')}, Severity: {cat.get('severity')}\n"
    if response.block_lists_match_result:
        for block_match in response.block_lists_match_result:
            decision_text += f"  - Blocked by list: {block_match.get('block_list_name')}, Item: {block_match.get('block_item_text')}\n"
    if response.sentiment is not None:
        decision_text += f"  - Sentiment: {response.sentiment}\n"

    if not response.categories and not response.block_lists_match_result and response.sentiment is None:
        decision_text += "  No specific issues detected.\n"

    prompt = f"Summarize the following text content moderation decisions:\n{decision_text}"

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes content moderation decisions."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error summarizing moderation decisions: {e}"
