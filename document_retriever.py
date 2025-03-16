from transformers import AutoTokenizer, AutoModel, pipeline
import faiss
import numpy as np
import torch
from Config_DB import connect_db, store_result, get_results

docs = [
    "Blockchain is a decentralized, distributed ledger technology.",
    "Proof of Work (PoW) is a consensus mechanism in blockchain.",
    "Smart contracts are self-executing contracts with terms directly written into code.",
    "Ethereum is a popular blockchain platform that supports smart contracts.",
]


model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def encode_sentences(sentences):
    tokens = tokenizer(sentences, padding=True, truncation=True, max_length=512, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**tokens)
    return outputs.last_hidden_state[:, 0, :].numpy()  # Take the [CLS] token embedding


doc_embeddings = encode_sentences(docs)

index = faiss.IndexFlatL2(doc_embeddings.shape[1])
index.add(np.array(doc_embeddings))


def retrieve(query, top_k=2):
    query_embedding = encode_sentences([query])
    distances, indices = index.search(np.array(query_embedding), top_k)
    return [docs[i] for i in indices[0]]


generator = pipeline("text-generation", model="gpt2")


def generate_answer(query):
    context = " ".join(retrieve(query))
    prompt = f"Answer the question based on the context:\nContext: {context}\nQuestion: {query}\nAnswer:"
    result = generator(prompt, max_length=150, num_return_sequences=1)
    return result[0]["generated_text"]


def fetch_results():
    return get_results()

if __name__ == "__main__":
    query = "How does Ethereum support smart contracts?"
    answer = generate_answer(query)
    store_result(query,answer)

    print(fetch_results())


