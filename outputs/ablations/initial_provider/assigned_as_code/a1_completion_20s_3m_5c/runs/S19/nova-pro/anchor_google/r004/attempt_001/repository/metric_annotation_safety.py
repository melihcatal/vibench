import re

def metric_annotation_safety(annotation):
    unsafe_patterns = [r'<script>', r'<style>', r'<iframe>', r'<object>', r'<embed>', r'<applet>']
    for pattern in unsafe_patterns:
        if re.search(pattern, annotation):
            return False
    return True
