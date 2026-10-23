import os
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient
from azure.ai.inference import EmbeddingsClient, ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential


def load_config(config=None):
    cfg = dict(config or {})
    cfg.setdefault('workspace_id', os.environ.get('AZURE_LOGS_WORKSPACE_ID'))
    cfg.setdefault('endpoint', os.environ.get('AZURE_LOGS_INGESTION_ENDPOINT'))
    cfg.setdefault('rule_id', os.environ.get('AZURE_LOGS_DCR_RULE_ID'))
    cfg.setdefault('stream_name', os.environ.get('AZURE_LOGS_STREAM_NAME'))
    cfg.setdefault('response_format', 'json')
    return cfg


def logs_query_client():
    return LogsQueryClient(DefaultAzureCredential())


def inference_clients(config=None):
    cfg = load_config(config)
    endpoint = cfg.get('ai_endpoint') or os.environ.get('AZURE_AI_INFERENCE_ENDPOINT')
    key = cfg.get('ai_key') or os.environ.get('AZURE_AI_INFERENCE_KEY')
    credential = AzureKeyCredential(key) if key else DefaultAzureCredential()
    return {
        'chat': ChatCompletionsClient(endpoint=endpoint, credential=credential),
        'embeddings': EmbeddingsClient(endpoint=endpoint, credential=credential),
    }
