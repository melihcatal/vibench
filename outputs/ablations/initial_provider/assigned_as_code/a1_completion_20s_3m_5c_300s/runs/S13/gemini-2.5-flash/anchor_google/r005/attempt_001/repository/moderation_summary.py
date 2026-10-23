import os
from typing import Dict, Any, List
from openai import OpenAI

def moderation_summary(moderation_decisions: List[Dict[str, Any]]) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Prepare the input for the summarization model
    decision_texts = []
    for i, decision in enumerate(moderation_decisions):
        decision_texts.append(f"Decision {i+1}: Text: {decision.get("text", "N/A")}, Is Unsafe: {decision.get("is_unsafe", "N/A")}, Scores: {decision.get("scores", "N/A")}")
    
    prompt = "Summarize the following moderation decisions:\n" + "\n".join(decision_texts)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Or "gpt-4"
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes moderation decisions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        return f"Error summarizing moderation decisions: {e}"
