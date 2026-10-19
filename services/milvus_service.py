from pymilvus import (
    connections,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
    utility
)
from config import (
    MILVUS_URI, 
    MILVUS_TOKEN,
    MILVUS_COLLECTION,
    EMBEDDING_DIM
)

class MilvusService:
    def get_total_vectors(self):
     self.collection.load()
     return self.collection.num_entities
    
    def __init__(self):
        """
        Connect to Zilliz Cloud Milvus instance.
        """
        connections.connect(
          alias="default",
          uri=MILVUS_URI,
          token=MILVUS_TOKEN
        )

        print("Connected to Zilliz Cloud successfully")
        self.collection = self.create_collection()

    def create_collection(self):
        """
        Creates a collection if it doesn't exist.
        """
        if utility.has_collection(MILVUS_COLLECTION):
            print(f"Collection '{MILVUS_COLLECTION}' exists. Using existing collection.")
            return Collection(MILVUS_COLLECTION)

        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=512),
            FieldSchema(name="chunk", dtype=DataType.INT64)
        ]
        schema = CollectionSchema(fields, description="RAG document collection")
        collection = Collection(name=MILVUS_COLLECTION, schema=schema)

        index_params = {"index_type": "IVF_FLAT", "metric_type": "COSINE", "params": {"nlist": 128}}
        collection.create_index("embedding", index_params=index_params)
        print(f"Collection '{MILVUS_COLLECTION}' created with IVF_FLAT index")
        return collection

    def insert_documents(self, texts, embeddings, metadatas, batch_size=128):
        """
        Insert documents in batches.
        """
        sources = [m["source"] for m in metadatas]
        chunks = [m["chunk"] for m in metadatas]
        total = len(texts)
        for i in range(0, total, batch_size):
            self.collection.insert([
                embeddings[i:i+batch_size],
                texts[i:i+batch_size],
                sources[i:i+batch_size],
                chunks[i:i+batch_size]
            ])
        self.collection.load()
        print(f"Inserted {total} vectors into collection '{MILVUS_COLLECTION}'")

    def search(self, query_embedding, k=3):
        """
        Search top-k similar embeddings.
        """
        self.collection.load()

        search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}

        results = self.collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param=search_params,
            limit=k,
            output_fields=["text", "source", "chunk"]
        )

        output = []

        for hit in results[0]:
            output.append({
                "text": hit.entity.get("text"),
                "score": hit.distance,   
                "metadata": {
                    "source": hit.entity.get("source"),
                    "chunk": hit.entity.get("chunk")
                }
            })

        return output