from openai import OpenAI
import os

def summarize_moderation_decisions(moderation_results: list[dict]):
    """
    Summarizes moderation decisions from a list of Azure AI Content Safety results
    using an OpenAI chat model.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    summary_texts = []
    for result in moderation_results:
        text = result.get('text')
        categories = result.get('categoriesAnalysis', [])
        violations = [f"{cat['category']} (Severity: {cat['severity']})" for cat in categories if cat['severity'] > 0]
        if violations:
            summary_texts.append(f"Content: '{text[:50]}...' - Violations: {', '.join(violations)}")
        else:
            summary_texts.append(f"Content: '{text[:50]}...' - No violations detected.")

    prompt_content = "Summarize the following moderation decisions. Highlight any detected violations and overall safety status:

" + "\n".join(summary_texts)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt_content,
            }
        ],
        model="gpt-4", # Using a common chat model
    )

    return chat_completion.choices[0].message.content
