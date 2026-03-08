from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_huggingface import HuggingFaceEmbeddings
from loguru import logger

from philoagents.config import settings

from .embeddings import get_embedding_model

Retriever = VectorStoreRetriever


def get_retriever(
    embedding_model_id: str,
    k: int = 3,
    device: str = "cpu",
) -> Retriever:
    """Creates and returns a FAISS vector search retriever.

    Args:
        embedding_model_id (str): The identifier for the embedding model to use.
        k (int, optional): Number of documents to retrieve. Defaults to 3.
        device (str, optional): Device to run the embedding model on. Defaults to "cpu".

    Returns:
        Retriever: A configured FAISS vector store retriever.
    """
    logger.info(
        f"Initializing retriever | model: {embedding_model_id} | device: {device} | top_k: {k}"
    )

    embedding_model = get_embedding_model(embedding_model_id, device)

    return get_faiss_retriever(embedding_model, k)


def get_faiss_retriever(
    embedding_model: HuggingFaceEmbeddings, k: int
) -> VectorStoreRetriever:
    """Loads a FAISS index from disk and returns a retriever.

    Args:
        embedding_model (HuggingFaceEmbeddings): The embedding model to use for vector search.
        k (int): Number of documents to retrieve.

    Returns:
        VectorStoreRetriever: A retriever backed by the persisted FAISS index.
    """
    vectorstore = FAISS.load_local(
        settings.FAISS_INDEX_PATH,
        embedding_model,
        allow_dangerous_deserialization=True,
    )

    return vectorstore.as_retriever(search_kwargs={"k": k})
