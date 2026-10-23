from google.cloud import language_v1
from identity_models import UserProfile
import os

# Initialize Google Cloud Natural Language client
client = language_v1.LanguageServiceClient.from_service_account_json(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
)


def profile_moderation(profile: UserProfile) -> bool:
    if not profile.display_name:
        return True

    document = language_v1.Document(
        content=profile.display_name, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.moderate_text(request={"document": document})

    for category in response.moderation_categories:
        if category.confidence > 0.8 and category.likely:
            return False

    return True
