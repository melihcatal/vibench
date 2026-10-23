import os
from typing import Iterable

from mistralai import Mistral


class QualitySummaryClient:
    def __init__(self):
        self.client = Mistral(api_key=os.environ.get('MISTRAL_API_KEY', ''))

    def summarize(self, issues: Iterable[str]) -> str:
        prompt = 'Summarize these translation quality issues concisely:
' + '
'.join(f'- {issue}' for issue in issues)
        response = self.client.chat.complete(model='mistral-small-latest', messages=[{'role': 'user', 'content': prompt}])
        return response.choices[0].message.content
