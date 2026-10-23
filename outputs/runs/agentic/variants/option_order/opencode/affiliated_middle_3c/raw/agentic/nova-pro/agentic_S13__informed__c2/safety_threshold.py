import ibm_watson


def safety_threshold(text):
    authenticator = ibm_watson.IAMAuthenticator("WATSONX_API_KEY")
    safety_service = ibm_watson.Safety(authenticator, "2021-06-01")
    safety_service.set_service_url("WATSONX_SERVICE_URL")
    response = safety_service.safety_check(text).get_result()
    return response
