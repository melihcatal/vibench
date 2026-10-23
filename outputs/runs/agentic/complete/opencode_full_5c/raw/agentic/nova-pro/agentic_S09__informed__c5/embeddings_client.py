import cohere


def get_cohere_client():
    return cohere.Client(os.getenv("COHERE_API_KEY"))
