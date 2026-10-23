from messaging_models import summarize_outcome
from azure.servicebus import ServiceBusClient


def message_summary(results):
    processed = len([result for result in results if result.get('status') == 'processed'])
    failed = len([result for result in results if result.get('status') == 'failed'])
    dead_lettered = len([result for result in results if result.get('status') == 'dead_lettered'])
    return summarize_outcome(processed=processed, failed=failed, dead_lettered=dead_lettered)
