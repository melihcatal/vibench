import boto3
import re

cw_logs = boto3.client("logs", region_name="us-west-2")

log_group_name = "MyLogGroup"


def check_log_text_safety(log_text):
    unsafe_patterns = [r"password", r"secret", r"confidential"]
    for pattern in unsafe_patterns:
        if re.search(pattern, log_text, re.IGNORECASE):
            return False
    return True


if __name__ == "__main__":
    log_text = "This is a sample log message with no sensitive information."
    is_safe = check_log_text_safety(log_text)
    print(is_safe)
