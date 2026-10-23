from model_client import client, converse_messages, load_config


def stream_completion(payload, config=None):
    cfg = load_config(config)
    llm, _ = client(cfg.__dict__)
    response = llm.converse_stream(
        modelId=cfg.model_id,
        messages=converse_messages(payload["prompt"]),
        inferenceConfig={"temperature": cfg.temperature, "maxTokens": cfg.max_tokens},
    )
    chunks = []
    for event in response["stream"]:
        if "contentBlockDelta" in event and "delta" in event["contentBlockDelta"]:
            delta = event["contentBlockDelta"]["delta"]
            if "text" in delta:
                chunks.append(delta["text"])
    return {"text": "".join(chunks)}
