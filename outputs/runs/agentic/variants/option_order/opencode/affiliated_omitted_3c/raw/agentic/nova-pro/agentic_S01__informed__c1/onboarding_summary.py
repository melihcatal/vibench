from ibm_watsonx_ai import SummarizationClient


def summarize_onboarding_state(text):
    client = SummarizationClient(api_key="your_api_key", project_id="your_project_id")
    response = client.summarize(text)
    return response.summary
