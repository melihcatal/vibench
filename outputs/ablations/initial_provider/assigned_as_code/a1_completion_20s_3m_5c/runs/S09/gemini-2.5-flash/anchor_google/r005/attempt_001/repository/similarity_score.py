import numpy as np

def similarity_score(payload):
    embedding1 = np.array(payload["embedding1"])
    embedding2 = np.array(payload["embedding2"])
    score = np.dot(embedding1, embedding2)
    return {"similarity_score": float(score)}
