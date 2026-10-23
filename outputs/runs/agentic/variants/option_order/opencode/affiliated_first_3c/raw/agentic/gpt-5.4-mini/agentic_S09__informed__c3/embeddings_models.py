def coerce_single_embedding(response):
    data = getattr(response, "data", response)
    first = data[0]
    return list(getattr(first, "embedding", first["embedding"]))


def coerce_embeddings(response):
    data = getattr(response, "data", response)
    result = []
    for item in data:
        result.append(list(getattr(item, "embedding", item["embedding"])))
    return result
