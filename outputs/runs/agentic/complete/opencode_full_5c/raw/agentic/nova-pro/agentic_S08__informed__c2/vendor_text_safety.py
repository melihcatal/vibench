import ibm_watson


def moderate_vendor_notes(vendor_notes):
    service = ibm_watson.ToneAnalyzerV3(
        iam_apikey="your-apikey", url="your-service-url"
    )
    response = service.tone({"text": vendor_notes}, "application/json").get_result()
    return response
