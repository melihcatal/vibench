import ibm_watson


def visual_safety_text(text):
    watsonx_guardrails = ibm_watson.GuardrailsV1(
        iam_apikey="WATSONX_API_KEY", url="WATSONX_URL"
    )
    response = watsonx_guardrails.evaluate(text=text)
    return response.get_result()
