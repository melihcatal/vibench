def normalize_embedding(vec: list[float]) -> list[float]:
    """L2-normalize an embedding vector.

    Args:
        vec (list[float]): Raw embedding list.

    Returns:
        list[float]: Normalized vector with unit length.
    """
    arr = np.array(vec, dtype=float)
    norm = np.linalg.norm(arr)
    if norm == 0:
        raise ValueError("Zero vector cannot be normalized")
    return (arr / norm).tolist()
