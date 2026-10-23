import os
import argparse
from security_client import SecurityClient
from security_models import ContentSafetyRequest, ContentSafetyResponse

def payload_safety_main():
    parser = argparse.ArgumentParser(description="Check decrypted text payloads for unsafe content using Azure AI Content Safety.")
    parser.add_argument("--text", required=True, help="The text payload to check for safety.")
    parser.add_argument("--content-safety-endpoint", required=False, 
                        help="The Azure Content Safety endpoint. Defaults to AZURE_CONTENT_SAFETY_ENDPOINT environment variable.")

    args = parser.parse_args()

    content_safety_endpoint = args.content_safety_endpoint or os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    if not content_safety_endpoint:
        raise ValueError("Azure Content Safety Endpoint not provided. Please set --content-safety-endpoint or AZURE_CONTENT_SAFETY_ENDPOINT environment variable.")

    client = SecurityClient()
    request = ContentSafetyRequest(text=args.text)

    try:
        response: ContentSafetyResponse = client.check_content_safety(request)
        print(f"Content Safety Check Result: {'SAFE' if response.is_safe else 'UNSAFE'}")
        print(f"Categories: {response.categories}")
        print(f"Severity Scores: {response.severity_scores}")
        if not response.is_safe:
            print("WARNING: Unsafe content detected!")
    except Exception as e:
        print(f"Content safety check failed: {e}")

if __name__ == "__main__":
    payload_safety_main()
