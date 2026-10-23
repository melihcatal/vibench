import watsonx_ai


def check_safety(text):
    client = watsonx_ai.Client(api_key=os.getenv("WATSONX_API_KEY"))
    result = client.content_safety.check(text)
    return result
