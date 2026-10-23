from google.cloud import translate_v3 as translate


def main():
    client = translate.TranslationServiceClient()
    parent = "projects/{}/locations/global".format(__import__("os").getenv("GOOGLE_CLOUD_PROJECT", "demo-project"))
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": ["Support-visible log message"],
            "mime_type": "text/plain",
            "target_language_code": "es",
        }
    )
    return response


if __name__ == "__main__":
    main()
