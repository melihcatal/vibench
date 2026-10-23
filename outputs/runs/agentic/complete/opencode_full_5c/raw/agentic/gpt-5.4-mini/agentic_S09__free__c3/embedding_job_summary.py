from embeddings_client import embedding_model, get_client


def embedding_job_summary(job_texts):
    response = get_client().embeddings.create(
        model=embedding_model(), input=list(job_texts)
    )
    return {
        "model": response.model,
        "count": len(response.data),
        "ids": [item.index for item in response.data],
    }


if __name__ == "__main__":
    print(embedding_job_summary(["a", "b", "c"]))
