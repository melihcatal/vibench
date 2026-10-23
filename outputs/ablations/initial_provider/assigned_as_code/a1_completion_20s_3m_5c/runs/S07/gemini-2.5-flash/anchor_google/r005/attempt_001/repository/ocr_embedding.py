import google.generativeai as genai

def ocr_embedding(payload, config=None):
    config = config or {}
    genai.configure(api_key=config["gemini_api_key"])

    text_to_embed = payload["text"]

    # The embedding model can be specified. For text, text-embedding-004 is a good choice.
    model_name = config.get("embedding_model", "models/embedding-001")

    result = genai.embed_content(model=model_name, content=text_to_embed)

    return {"embedding": result['embedding'], "original_text": text_to_embed}
