from openai import OpenAI

from storage_models import normalize_config, normalize_payload, object_response


def asset_metadata_embedding(payload, config=None):
    cfg = normalize_config(config)
    pl = normalize_payload(payload)
    client = OpenAI(api_key=cfg['openai_api_key'])
    text = ' '.join(str(pl.get(key, '')) for key in ('object_name', 'metadata', 'text'))
    embedding = client.embeddings.create(model=cfg.get('openai_embedding_model', 'text-embedding-3-small'), input=text)
    return object_response(pl['object_name'], embedding=embedding.data[0].embedding)
