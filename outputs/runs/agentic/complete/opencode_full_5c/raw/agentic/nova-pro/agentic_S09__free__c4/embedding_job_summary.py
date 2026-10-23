def summarize_embedding_job_results(results):
    summary = {
        "total_embeddings": len(results),
        "successful_embeddings": sum(1 for r in results if r is not None),
        "failed_embeddings": sum(1 for r in results if r is None),
    }
    return summary
