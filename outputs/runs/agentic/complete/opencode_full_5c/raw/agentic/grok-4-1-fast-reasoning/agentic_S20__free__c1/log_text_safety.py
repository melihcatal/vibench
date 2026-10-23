import os
from openai import OpenAI


def check_log_text_safety(log_text: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(input=log_text, model="text-moderation-latest")
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories,
        "category_scores": result.category_scores,
    }


if __name__ == "__main__":
    test_logs = [
        "Normal log: user logged in.",
        "Potentially unsafe: contains hate speech against group X.",
    ]
    for log in test_logs:
        safety = check_log_text_safety(log)
        print(f"Log: {log[:50]}... Safety: {safety['flagged']}")
