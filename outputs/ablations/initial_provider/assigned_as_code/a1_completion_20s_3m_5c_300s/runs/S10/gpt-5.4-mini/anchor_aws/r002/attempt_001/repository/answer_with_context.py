from model_client import client, converse_messages, extract_converse_text, load_config
from model_models import build_qa_prompt


def answer_with_context(payload, config=None):
    cfg = load_config(config)
    llm, _ = client(cfg.__dict__)
    prompt = build_qa_prompt(payload["question"], payload["context"])
    response = llm.converse(
        modelId=cfg.model_id,
        messages=converse_messages(prompt),
        inferenceConfig={"temperature": cfg.temperature, "maxTokens": cfg.max_tokens},
    )
    return {"answer": extract_converse_text(response)}
