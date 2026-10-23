from watsonx.ai import WatsonxClient


def moderate_vendor_notes(vendor_notes):
    client = WatsonxClient(
        api_key=os.getenv("WATSONX_API_KEY"), project_id=os.getenv("WATSONX_PROJECT_ID")
    )
    result = client.moderate(vendor_notes)
    return result
