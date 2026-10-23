import watsonx


def check_unsafe_content(text):
    client = watsonx.Client(
        api_key=os.getenv("WATSONX_API_KEY"), project_id=os.getenv("WATSONX_PROJECT_ID")
    )
    response = client.moderation.create(text=text)
    return response.results[0].flagged


if __name__ == "__main__":
    print(check_unsafe_content("This content is inappropriate."))
