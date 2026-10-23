from google.cloud import aiplatform_v1


def main():
    client = aiplatform_v1.PredictionServiceClient()
    endpoint = client.endpoint_path(project=__import__("os").getenv("GOOGLE_CLOUD_PROJECT", "demo-project"), location="us-central1", endpoint="1234567890")
    instances = [{"content": "selected log message for semantic retrieval"}]
    response = client.predict(endpoint=endpoint, instances=instances)
    return response


if __name__ == "__main__":
    main()
