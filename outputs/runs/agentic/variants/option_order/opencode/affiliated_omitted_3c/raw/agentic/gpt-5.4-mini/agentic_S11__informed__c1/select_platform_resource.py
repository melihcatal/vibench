import json

from model_client import bedrock_client, load_settings


def select_platform_resource():
    settings = load_settings()
    client = bedrock_client()
    if settings.profile_arn:
        return {"profileArn": settings.profile_arn, "modelId": settings.model_id}
    response = client.get_foundation_model(modelIdentifier=settings.model_id)
    return {"modelId": response["modelId"], "response": response}


def main():
    print(json.dumps(select_platform_resource(), default=str))


if __name__ == "__main__":
    main()
