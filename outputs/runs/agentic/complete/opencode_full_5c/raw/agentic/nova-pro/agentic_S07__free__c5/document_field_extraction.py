import re


def extract_fields(text):
    fields = {}
    # Example regex patterns for field extraction
    fields["name"] = re.search(r"Name: (.+)", text)
    fields["address"] = re.search(r"Address: (.+)", text)
    return fields
