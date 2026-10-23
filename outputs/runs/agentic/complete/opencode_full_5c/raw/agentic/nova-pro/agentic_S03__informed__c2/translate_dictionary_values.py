import boto3


def translate_dictionary_values(dictionary, source_lang, target_lang):
    client = boto3.client("translate")
    translated_dict = {}
    for key, value in dictionary.items():
        response = client.translate_text(
            Text=value, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang
        )
        translated_dict[key] = response["TranslatedText"]
    return translated_dict


if __name__ == "__main__":
    print(translate_dictionary_values({"greeting": "Hello, world!"}, "en", "fr"))
