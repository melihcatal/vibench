from observability_client import OpenAIClient
from observability_models import SafetyCheckResult, LogEvent
from typing import List

def check_log_safety(log_messages: List[str]) -> List[SafetyCheckResult]:
    openai_client = OpenAIClient()
    results: List[SafetyCheckResult] = []

    for message in log_messages:
        moderation_output = openai_client.check_safety(message)
        
        is_safe = not moderation_output["flagged"]
        flagged_categories = [category for category, flagged in moderation_output["categories"].items() if flagged]
        moderation_scores = moderation_output["category_scores"]

        results.append(SafetyCheckResult(
            is_safe=is_safe,
            flagged_categories=flagged_categories,
            moderation_score=moderation_scores
        ))
    return results

if __name__ == "__main__":
    # Example log messages
    sample_log_messages = [
        "User 'testuser' logged in successfully from 192.168.1.1.",
        "Found a potentially harmful script injection attempt from IP 1.2.3.4: <script>alert('XSS')</script>",
        "Content with hate speech detected: \"I hate everyone who disagrees with me!\"",
        "System health check passed with no issues."
    ]

    print("Checking log messages for unsafe content...")
    safety_results = check_log_safety(sample_log_messages)

    for i, result in enumerate(safety_results):
        print(f"\n--- Log Message {i+1} ---")
        print(f"Original: {sample_log_messages[i]}")
        print(f"Is Safe: {result.is_safe}")
        if not result.is_safe:
            print(f"Flagged Categories: {', '.join(result.flagged_categories)}")
            print(f"Moderation Scores: {result.moderation_score}")
        else:
            print("No unsafe content detected.")
