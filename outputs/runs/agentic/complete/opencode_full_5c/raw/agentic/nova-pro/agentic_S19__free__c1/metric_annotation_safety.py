import re


def check_metric_annotation_safety(annotation):
    unsafe_patterns = [
        r"<script>",
        r"<style>",
        r"<iframe>",
        r"javascript:",
        r"vbscript:",
        r"data:",
        r"<object>",
        r"<embed>",
        r"<applet>",
        r"<marq>",
        r"<xml>",
        r"<![CDATA[",
        r"<!--",
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, annotation):
            return False
    return True
