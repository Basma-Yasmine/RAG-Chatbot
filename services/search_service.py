from services.embedding_service import get_embeddings

def retrieve_context(query, milvus_service, k=3):

    query_embedding = get_embeddings([query])[0]
    results = milvus_service.search(query_embedding, k)

    context = "\n\n".join([r["text"] for r in results])

    sources = []

    for r in results:
        sources.append({
            "source": r["metadata"]["source"],
            "chunk": r["metadata"]["chunk"],
            "text": r["text"],
            "score": r["score"]
        })

    return context, sources