import watsonx


def check_unsafe_content(text):
    client = watsonx.Client(
        apikey=os.getenv("WATSONX_API_KEY"), project_id=os.getenv("WATSONX_PROJECT_ID")
    )
    response = client.text_content_safety(text)
    return response["results"]
