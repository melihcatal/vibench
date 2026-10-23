import os
import boto3

def check_output_safety(text: str) -> dict:
    """
    Checks platform model output for unsafe content using Amazon Comprehend Toxicity.
    Note: Bedrock Guardrails would be a more direct integration for Bedrock outputs,
    but Comprehend Toxicity is used here as an alternative from the options.
    """
    comprehend_client = boto3.client(
        service_name="comprehend",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

    try:
        # Comprehend DetectToxicContent only supports 'en' language code
        response = comprehend_client.detect_toxic_content(
            Text=text,
            LanguageCode='en'
        )
        return response
    except Exception as e:
        print(f"Error detecting toxic content with Amazon Comprehend: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage (requires AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION to be set in environment)
    safe_text = "The quick brown fox jumps over the lazy dog."
    unsafe_text = "I hate this stupid world!" # Example of potentially toxic content

    print("Checking safe text:")
    safety_report_safe = check_output_safety(safe_text)
    print(safety_report_safe)

    print("
Checking unsafe text:")
    safety_report_unsafe = check_output_safety(unsafe_text)
    print(safety_report_unsafe)
