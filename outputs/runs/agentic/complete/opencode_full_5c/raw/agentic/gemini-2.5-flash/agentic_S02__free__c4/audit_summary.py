import os
import boto3


def summarize_audit_event_notes(text: str, language_code: str = "en") -> str:
    # AWS Comprehend client
    # Ensure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set in environment variables
    # or configured via AWS CLI/SDK default profiles.
    comprehend = boto3.client(
        "comprehend",
        region_name=os.environ.get(
            "AWS_REGION", "us-east-1"
        ),  # AWS_REGION is provider-specific
    )

    try:
        # Detect key phrases to get a summary of the text
        response = comprehend.detect_key_phrases(Text=text, LanguageCode=language_code)
        key_phrases = [phrase["Text"] for phrase in response["KeyPhrases"]]
        return "; ".join(key_phrases)
    except Exception as e:
        raise Exception(
            f"Failed to summarize audit event notes using AWS Comprehend: {e}"
        )


if __name__ == "__main__":
    example_notes = "User jane.doe logged in from IP 203.0.113.42. Multi-factor authentication was successful. Attempted to access sensitive resource but was denied due to insufficient permissions. A new session token was issued."
    try:
        summary = summarize_audit_event_notes(example_notes)
        print(f"Summary of audit notes: {summary}")
    except Exception as e:
        print(f"Error: {e}")
