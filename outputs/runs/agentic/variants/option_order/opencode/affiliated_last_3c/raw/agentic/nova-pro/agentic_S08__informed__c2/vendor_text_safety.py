import watsonx_guardrails


def vendor_text_safety(vendor_text):
    safety_result = watsonx_guardrails.check_safety(vendor_text)
    return safety_result
