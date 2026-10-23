import os
import ibm_watson

authenticator = ibm_watson.IAMAuthenticator(os.getenv('WATSONX_API_KEY'))
safety_service = ibm_watson.TextModerationV1(authenticator)
safety_service.set_service_url('https://api.us-south.text-moderation.watson.cloud.ibm.com')

def vendor_text_safety(text):
    response = safety_service.classify(text).get_result()
    return response