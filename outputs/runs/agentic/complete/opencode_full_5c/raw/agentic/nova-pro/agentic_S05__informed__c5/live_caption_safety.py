import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

os.environ["WATSONX_API_KEY"] = "your-watsonx-api-key"
os.environ["WATSONX_PROJECT_ID"] = "your-watsonx-project-id"


def check_safety(text):
    authenticator = IAMAuthenticator(os.getenv("WATSONX_API_KEY"))
    language_translator = LanguageTranslatorV3(
        version="2023-05-15", authenticator=authenticator
    )
    language_translator.set_service_url(
        "https://api.us-south.language-translator.watson.cloud.ibm.com/instances/your-instance-id"
    )
    result = language_translator.translate(text=text, model_id="en-es").get_result()
    return result


if __name__ == "__main__":
    print(check_safety("Hello, world!"))
