import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import (
    Features,
    EntitiesOptions,
    KeywordsOptions,
)

os.environ["WATSONX_API_KEY"] = "your-api-key"
os.environ["WATSONX_PROJECT_ID"] = "your-project-id"
authenticator = IAMAuthenticator(os.environ["WATSONX_API_KEY"])
nlu = NaturalLanguageUnderstandingV1(version="2021-08-01", authenticator=authenticator)
nlu.set_service_url(
    "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/your-instance-id"
)
