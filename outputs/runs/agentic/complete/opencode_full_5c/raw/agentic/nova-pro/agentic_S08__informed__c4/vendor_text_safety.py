from watsonx_guardrails import WatsonxGuardrails


def vendor_text_safety(vendor_text):
    guardrails = WatsonxGuardrails(WATSONX_API_KEY, WATSONX_PROJECT_ID)
    response = guardrails.moderate(vendor_text)
    return response.is_safe
