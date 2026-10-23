import os
from openai import OpenAI

SAMPLE_LOG_TEXTS = [
    "Normal log: User logged in.",
    "Suspicious: Attempted SQL injection detected in query."
]

def check_logs_for_safety(log_texts):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    results = []
    for text in log_texts:
        response = client.moderations.create(
            input=text,
            model="text-moderation-3.5-latest"
        )
        result = response.results[0]
        results.append({
            "input": text,
            "flagged": result.flagged,
            "categories": dict(result.categories),
            "category_scores": dict(result.category_scores)
        })
    print(results)
    return results

if __name__ == "__main__":
    check_logs_for_safety(SAMPLE_LOG_TEXTS)