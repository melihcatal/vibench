import os
from typing import List
from observability_client import get_azure_content_moderator_client

def check_log_text_safety(log_messages: List[str]):
    """Checks selected log message text for unsafe content using Azure Content Moderator."""
    client = get_azure_content_moderator_client()

    if not client:
        print("Azure Content Moderator client not initialized. Cannot check text safety.")
        return []

    findings = []
    for i, message in enumerate(log_messages):
        print(f"Checking message {i+1}/{len(log_messages)}: '{message[:50]}...'")
        try:
            # The text_moderation.screen_text method provides content moderation.
            # We can enable different classifications (e.g., adult, racy, personal data)
            # and review suggestions.
            screen_result = client.text_moderation.screen_text(
                text_content=message,
                language="eng",
                autocorrect=True,
                pii=True, # Enable Personal Identifiable Information detection
            )

            is_unsafe = False
            violations = []

            # Check for adult or racy content
            if screen_result.adult_classification and screen_result.adult_classification.review_recommended:
                is_unsafe = True
                violations.append(f"Adult content detected (score: {screen_result.adult_classification.score})")
            if screen_result.racy_classification and screen_result.racy_classification.review_recommended:
                is_unsafe = True
                violations.append(f"Racy content detected (score: {screen_result.racy_classification.score})")
            
            # Check for profanity terms
            if screen_result.terms:
                is_unsafe = True
                violations.append(f"Profanity terms detected: {[term.term for term in screen_result.terms]}")

            # Check for PII
            if screen_result.p_ii:
                pii_data = []
                if screen_result.p_ii.email:
                    pii_data.extend([e.text for e in screen_result.p_ii.email])
                if screen_result.p_ii.phone:
                    pii_data.extend([p.text for p in screen_result.p_ii.phone])
                if screen_result.p_ii.address:
                    pii_data.extend([a.text for a in screen_result.p_ii.address])
                if screen_result.p_ii.ip_address:
                    pii_data.extend([ip.text for ip in screen_result.p_ii.ip_address])
                
                if pii_data:
                    is_unsafe = True
                    violations.append(f"Personal Identifiable Information (PII) detected: {pii_data}")

            if is_unsafe:
                findings.append({
                    "message_index": i,
                    "message": message,
                    "unsafe": True,
                    "violations": violations
                })
            else:
                findings.append({
                    "message_index": i,
                    "message": message,
                    "unsafe": False,
                    "violations": []
                })

        except Exception as e:
            print(f"Error checking text safety for message '{message[:50]}...': {e}")
            findings.append({
                "message_index": i,
                "message": message,
                "unsafe": True, # Mark as unsafe if an error occurs to be safe
                "violations": [f"Error during moderation: {e}"]
            })

    print("Log text safety check completed using Azure Content Moderator.")
    for finding in findings:
        print(f"  Message: '{finding['message'][:70]}...', Unsafe: {finding['unsafe']}, Violations: {finding['violations']}")
    return findings

if __name__ == "__main__":
    # Example usage
    # Set these environment variables before running
    # os.environ["AZURE_CONTENT_MODERATOR_ENDPOINT"] = "https://YOUR_RESOURCE_NAME.cognitiveservices.azure.com/"
    # os.environ["AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY"] = "YOUR_SUBSCRIPTION_KEY"

    if not os.getenv("AZURE_CONTENT_MODERATOR_ENDPOINT") or not os.getenv("AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY"):
        print("Please set AZURE_CONTENT_MODERATOR_ENDPOINT and AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY environment variables.")
    else:
        sample_log_messages = [
            "User 'baduser' attempted to inject malicious SQL: DROP TABLE users;",
            "Normal log message: Processing request for user id 123.",
            "Alert! Potential data leak: credit card number 1234-5678-9012-3456 detected.",
            "User 'john.doe@example.com' logged in from IP 192.168.1.100.",
            "This message contains some offensive language that should be flagged."
        ]
        safety_findings = check_log_text_safety(sample_log_messages)
        print("\n--- Safety Findings ---")
        for finding in safety_findings:
            print(finding)
