import ibm_watson


def vendor_text_safety(vendor_notes):
    authenticator = ibm_watson.IAMAuthenticator(os.environ["WATSONX_API_KEY"])
    service = ibm_watson.ToneAnalyzerV3(
        version="2021-09-01", authenticator=authenticator
    )
    service.set_service_url(os.environ["WATSONX_URL"])
    response = service.tone(
        {"text": vendor_notes}, content_type="application/json"
    ).get_result()
    return response
