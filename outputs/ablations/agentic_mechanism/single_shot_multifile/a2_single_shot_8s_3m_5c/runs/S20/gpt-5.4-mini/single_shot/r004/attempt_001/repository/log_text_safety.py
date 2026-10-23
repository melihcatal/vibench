from google.cloud import language_v1


def main():
    client = language_v1.LanguageServiceClient()
    text = "This is a support-visible log message"
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_syntax(request={"document": document, "encoding_type": language_v1.EncodingType.UTF16})
    return response


if __name__ == "__main__":
    main()
