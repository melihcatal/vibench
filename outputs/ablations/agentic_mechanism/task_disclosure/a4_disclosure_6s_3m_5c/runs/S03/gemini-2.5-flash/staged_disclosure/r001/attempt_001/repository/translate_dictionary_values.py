from google.cloud import translate_v3 as translate

def translate_dictionary_values(input_dict, target_language, project_id):
    """
    Translates the values of a dictionary using Google Cloud Translation, preserving keys.

    Args:
        input_dict (dict): The dictionary whose values are to be translated.
        target_language (str): The language code to translate the values into (e.g., "es" for Spanish).
        project_id (str): Your Google Cloud project ID.

    Returns:
        dict: A new dictionary with the translated values and original keys.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"
    translated_dict = {}

    for key, value in input_dict.items():
        if isinstance(value, str):
            response = client.translate_text(
                request={
                    "parent": parent,
                    "contents": [value],
                    "target_language_code": target_language,
                }
            )
            for translation in response.translations:
                translated_dict[key] = translation.translated_text
        else:
            translated_dict[key] = value  # Preserve non-string values
    return translated_dict

if __name__ == "__main__":
    # Example usage:
    # Replace 'YOUR_PROJECT_ID' with your actual Google Cloud Project ID
    # Ensure you have authenticated with Google Cloud (e.g., `gcloud auth application-default login`)

    # from google.oauth2 import service_account
    # credentials = service_account.Credentials.from_service_account_file('path/to/your/service_account.json')
    # client = translate.TranslationServiceClient(credentials=credentials)

    my_dict = {
        "hello": "Hello world",
        "goodbye": "Goodbye everyone",
        "number": 123,
        "list_example": ["item1", "item2"]
    }
    project_id = "YOUR_PROJECT_ID"  # <<< IMPORTANT: Replace with your Google Cloud Project ID
    target_lang = "fr"

    if project_id == "YOUR_PROJECT_ID":
        print("Please replace 'YOUR_PROJECT_ID' with your actual Google Cloud Project ID in the script.")
    else:
        print(f"Original dictionary: {my_dict}")
        translated_result = translate_dictionary_values(my_dict, target_lang, project_id)
        print(f"Translated dictionary (to {target_lang}): {translated_result}")
