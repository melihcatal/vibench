import os
from typing import Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


class AmazonTranslateClient:
    """Client helper for Amazon Translate."""

    def __init__(self):
        self.client = boto3.client(
            'translate',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )

    def translate_text(self, text: str, source_lang: str, target_lang: str) -> Optional[str]:
        try:
            response = self.client.translate_text(
                Text=text,
                SourceLanguageCode=source_lang,
                TargetLanguageCode=target_lang
            )
            return response.get('TranslatedText')
        except (BotoCoreError, ClientError) as e:
            print(f"Translation error: {e}")
            return None