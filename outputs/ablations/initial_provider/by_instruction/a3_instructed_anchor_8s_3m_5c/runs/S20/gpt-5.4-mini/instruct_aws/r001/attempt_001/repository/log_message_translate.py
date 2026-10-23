import boto3


def translate_message(text: str, source: str = "en", target: str = "es") -> str:
    client = boto3.client("translate", region_name="us-east-1")
    response = client.translate_text(Text=text, SourceLanguageCode=source, TargetLanguageCode=target)
    return response.get("TranslatedText", "")


if __name__ == "__main__":
    print(translate_message("example"))
