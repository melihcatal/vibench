def generate_summary(labels, caption, text_segments):
    summary_parts = []
    if caption:
        summary_parts.append(caption)
    if labels:
        labels_str = ", ".join(labels)
        summary_parts.append(f"Labels: {labels_str}")
    if text_segments:
        summary_parts.append(f"Extracted Text: {\" \\n\".join(text_segments)}")
    return "\\n\".join(summary_parts)
