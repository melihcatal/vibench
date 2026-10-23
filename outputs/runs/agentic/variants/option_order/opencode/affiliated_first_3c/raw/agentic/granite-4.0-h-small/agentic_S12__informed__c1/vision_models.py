# Define local request, response, and normalization helpers for Static Image and Visual Understanding
import os


def normalize_labels(raw_labels):
    """Normalize and deduplicate label strings."""
    return sorted(set(label.lower().strip() for label in raw_labels))


def normalize_description(raw_description):
    """Trim whitespace and ensure a concise description."""
    return raw_description.strip().capitalize()


# Example placeholder for text extraction normalization (Textract returns list of lines)
def normalize_text(raw_lines):
    """Join lines and remove empty strings."""
    return " ".join(filter(None, raw_lines)).strip()
