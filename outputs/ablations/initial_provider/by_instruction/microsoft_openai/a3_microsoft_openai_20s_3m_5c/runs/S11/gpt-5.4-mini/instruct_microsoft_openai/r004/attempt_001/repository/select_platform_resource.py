import os

from model_client import resolve_platform_resource


def select_platform_resource(preferred: str | None = None) -> str:
    return resolve_platform_resource(preferred or os.getenv("AZURE_OPENAI_DEPLOYMENT"))


if __name__ == "__main__":
    print(select_platform_resource())
