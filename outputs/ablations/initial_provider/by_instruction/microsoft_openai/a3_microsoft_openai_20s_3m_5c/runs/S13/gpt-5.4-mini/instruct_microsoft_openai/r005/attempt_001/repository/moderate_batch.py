from safety_client import moderate_batch_openai


def moderate_batch(texts):
    return moderate_batch_openai(texts)
