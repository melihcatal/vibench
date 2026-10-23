from transformers import AutoModel, AutoTokenizer

def embed_transcript_segments(segments):
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model = AutoModel.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    embeddings = []
    for segment in segments:
        inputs = tokenizer(segment, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        embeddings.append(embedding)
    return embeddings

if __name__ == "__main__":
    segments = ["This is the first segment.", "Here is another segment."]
    embeddings = embed_transcript_segments(segments)
    print(embeddings)