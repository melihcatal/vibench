from safety_client import AzureContentSafetyClient
from safety_models import normalize_thresholds


client = AzureContentSafetyClient()


def safety_threshold(scores, thresholds):
    return client.threshold_allow(scores, normalize_thresholds(thresholds))
