import json
import os
import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = "chunks.json"
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "amherst_guide"
MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 4  # start with 4, tune after seeing real results

# cached so load_vector_store() doesn't reload the model on every retrieve() call
_cached_collection = None
_cached_model = None


def load_chunks():
    if not os.path.exists(CHUNKS_FILE):
        raise FileNotFoundError(f"'{CHUNKS_FILE}' not found. Run ingest_chunks.py first.")
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# embeds all chunks and loads them into ChromaDB with metadata
def build_vector_store():
    global _cached_collection, _cached_model

    chunks = load_chunks()
    model = SentenceTransformer(MODEL_NAME)

    client = chromadb.PersistentClient(path=CHROMA_DIR)

    # wipe and recreate so stale data from earlier runs doesn't accumulate
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    # cosine distance works better for semantic similarity than the default L2
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    documents = [chunk["text"] for chunk in chunks]
    ids = [f'{chunk["source_file"]}_{chunk["chunk_index"]}' for chunk in chunks]

    # store source name and chunk position at minimum for attribution later
    metadatas = [
        {
            "source_file": chunk["source_file"],
            "title": chunk["title"],
            "source": chunk["source"],
            "url": chunk["url"],
            "chunk_index": chunk["chunk_index"],
        }
        for chunk in chunks
    ]

    print(f"Embedding {len(documents)} chunks with '{MODEL_NAME}'...")
    embeddings = model.encode(documents, show_progress_bar=True).tolist()

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Saved {collection.count()} chunks to ChromaDB.")

    # warm the cache so subsequent retrieve() calls don't reload from disk
    _cached_collection = collection
    _cached_model = model

    return collection, model


def load_vector_store():
    global _cached_collection, _cached_model

    if _cached_collection is not None and _cached_model is not None:
        return _cached_collection, _cached_model

    if not os.path.exists(CHROMA_DIR):
        raise FileNotFoundError(
            f"'{CHROMA_DIR}' not found. Run build_vector_store() first."
        )

    model = SentenceTransformer(MODEL_NAME)
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)

    _cached_collection = collection
    _cached_model = model

    return collection, model


# accepts a query string and returns the top-k most relevant chunks
# with source info. collection and model can be passed in so Milestone 5 doesn't
# reload on every call
def retrieve(query, top_k=TOP_K, collection=None, model=None):
    if collection is None or model is None:
        collection, model = load_vector_store()

    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    retrieved = []
    for doc, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        retrieved.append({
            "text": doc,
            "metadata": metadata,
            "distance": distance,  # cosine distance: lower = more relevant
        })

    return retrieved


if __name__ == "__main__":
    build_vector_store()

    # load once and reuse across all eval queries
    collection, model = load_vector_store()

    test_questions = [
        "What academic support resources does Amherst list for students?",
        "What do students say about Amherst social life or campus community?",
        "What advice do students give incoming first-year students at Amherst?",
        "How do meal plans work at Amherst College dining hall?",
        "What do students say about things to do in Amherst town?",
    ]

    for question in test_questions:
        print("\n" + "=" * 80)
        print(f"QUERY: {question}")
        print("=" * 80)

        results = retrieve(question, top_k=TOP_K, collection=collection, model=model)

        for i, result in enumerate(results, start=1):
            meta = result["metadata"]
            print(f"\nResult {i}  (cosine dist: {result['distance']:.4f})")
            print(f"Title : {meta['title']}")
            print(f"Source: {meta['source']}")
            print(f"URL   : {meta['url']}")
            print(f"File  : {meta['source_file']}  chunk #{meta['chunk_index']}")
            snippet = result["text"][:300].replace("\n", " ")
            print(f"Text  : {snippet}{'...' if len(result['text']) > 300 else ''}")