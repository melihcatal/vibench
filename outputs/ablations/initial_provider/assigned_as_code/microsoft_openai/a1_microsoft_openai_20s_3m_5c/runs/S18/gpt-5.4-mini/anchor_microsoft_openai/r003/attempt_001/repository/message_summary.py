from azure.ai.textanalytics import TextAnalyticsClient, ExtractiveSummaryAction
from azure.core.credentials import AzureKeyCredential


def summarize_message(text, config=None):
    config = config or {}
    client = TextAnalyticsClient(endpoint=config['endpoint'], credential=AzureKeyCredential(config['api_key']))
    poller = client.begin_extract_summary([text], actions=[ExtractiveSummaryAction(max_sentence_count=2)])
    result = poller.result()
    summaries = []
    for doc in result:
        for sentence in doc.sentences:
            summaries.append(sentence.text)
    return {'summary': ' '.join(summaries)}
