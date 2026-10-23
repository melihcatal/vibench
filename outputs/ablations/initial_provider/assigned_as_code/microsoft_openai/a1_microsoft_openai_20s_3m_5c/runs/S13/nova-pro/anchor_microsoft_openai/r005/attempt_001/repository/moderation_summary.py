from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from summarizer import Summarizer


def moderation_summary(payloads, config=None):
    config = config or {}
    with ContentSafetyClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        summarizer = Summarizer()
        summaries = []
        for payload in payloads:
            response = client.analyze_text(AnalyzeTextOptions(text=payload['text'], output_type='EightSeverityLevels'))
            summary = summarizer(payload['text'], ratio=0.2)
            summaries.append({'text': payload['text'], 'summary': summary, 'toxicity': max((category.severity for category in response.categories_analysis), default=0) / 7})
    return summaries