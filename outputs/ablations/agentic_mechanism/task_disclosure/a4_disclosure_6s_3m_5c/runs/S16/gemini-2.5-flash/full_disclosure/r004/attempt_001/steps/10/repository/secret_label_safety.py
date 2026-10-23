from google.cloud import dlp_v2

def check_unsafe_text(text: str) -> bool:
    client = dlp_v2.DlpServiceClient()
    project = "YOUR_PROJECT_ID"  # Replace with your Google Cloud Project ID

    # Define the info types to scan for. These are common sensitive data types.
    info_types = [
        {"name": "EMAIL_ADDRESS"},
        {"name": "PHONE_NUMBER"},
        {"name": "CREDIT_CARD_NUMBER"},
        {"name": "IP_ADDRESS"},
        {"name": "US_SOCIAL_SECURITY_NUMBER"},
        {"name": "US_DRIVERS_LICENSE_NUMBER"},
        {"name": "DATE_OF_BIRTH"},
        {"name": "PERSON_NAME"},
    ]

    # Create a configuration dictionary to specify the types of content to inspect.
    inspect_config = {
        "info_types": info_types,
        "include_quote": True
    }

    # Create a content item to inspect.
    item = {"value": text}

    try:
        response = client.inspect_content(
            request={
                "parent": f"projects/{project}/locations/global",
                "inspect_config": inspect_config,
                "item": item,
            }
        )

        if response.result.findings:
            return True  # Unsafe text (sensitive info) found
        else:
            return False  # No unsafe text found

    except Exception as e:
        # In a real-world scenario, you might want to log the error
        # or handle it more gracefully. For this task, we'll return True
        # if an error occurs during the check, as a precaution.
        print(f"Error during DLP inspection: {e}")
        return True
