from transformers import AutoModel, AutoTokenizer

def generate_embedding(text):
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model = AutoModel.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    embedding = outputs.last_hidden_state.mean(dim=1)
    return embedding.detach().numpy()

if __name__ == "__main__":
    sample_text = "This is a sample text to generate an embedding."
    embedding = generate_embedding(sample_text)
    print(embedding)