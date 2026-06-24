from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
import os


def create_vector_store():

    documents = []

    for file_name in os.listdir("resumes"):

        file_path = os.path.join(
            "resumes",
            file_name
        )

        with open(
                file_path,
                "r",
                encoding="utf-8"
        ) as file:

            content = file.read()

            documents.append(
                Document(
                    page_content=content,
                    metadata={
                        "file_name": file_name
                    }
                )
            )

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.from_documents(
        documents,
        embeddings
    )

    vector_store.save_local(
        "vector_db"
    )

    print(
        "Vector Store Created Successfully"
    )


def search_resumes(query):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.load_local(
        "vector_db",
        embeddings,
        allow_dangerous_deserialization=True
    )

    results = vector_store.similarity_search(
        query,
        k=5
    )

    return results