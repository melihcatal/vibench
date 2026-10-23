from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator("WATSONX_API_KEY")
discovery = DiscoveryV2(version="2023-04-27", authenticator=authenticator)


def extract_fields(text):
    response = discovery.analyze_document(
        project_id="your-project-id", collection_id="your-collection-id", file=text
    ).get_result()
    return response["results"][0]["enriched_text"]["entities"]
