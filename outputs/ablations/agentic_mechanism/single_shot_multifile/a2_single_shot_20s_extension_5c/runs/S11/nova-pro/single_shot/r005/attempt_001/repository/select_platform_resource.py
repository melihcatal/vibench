import os

def select_platform_resource():
    model_id = os.getenv('TEXT_ANALYTICS_MODEL_ID', 'latest')
    return model_id