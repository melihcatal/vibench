import re


def check_message_safety(payload):
    unsafe_patterns = [
        r"<script[^>]*>.*?<\/script>",
        r"<style[^>]*>.*?<\/style>",
        r"<iframe[^>]*>.*?<\/iframe>",
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, payload):
            return False
    return True