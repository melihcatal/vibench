from observability_client import get_dlp_client, get_gcp_project_id


def check_log_for_unsafe_content(log_message: str):
    dlp_client = get_dlp_client()
    project_id = get_gcp_project_id()

    parent = f"projects/{project_id}"

    item = {"value": log_message}

    inspect_config = {
        "info_types": [
            {"name": "EMAIL_ADDRESS"},
            {"name": "PHONE_NUMBER"},
            {"name": "CREDIT_CARD_NUMBER"},
        ]
    }

    request = {
        "parent": parent,
        "item": item,
        "inspect_config": inspect_config,
    }

    response = dlp_client.inspect_content(request=request)

    if response.result.findings:
        print(f"Unsafe content found in log message: '{log_message}'")
        for finding in response.result.findings:
            print(f"\tInfo type: {finding.info_type.name}")
            print(f"\tLikelihood: {finding.likelihood}")
    else:
        print("No unsafe content detected.")


if __name__ == "__main__":
    safe_log = "User logged in successfully from IP 192.168.0.1"
    unsafe_log = "User contact: myemail@example.com, phone 555-123-4567"
    check_log_for_unsafe_content(safe_log)
    check_log_for_unsafe_content(unsafe_log)
