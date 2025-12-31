from pathlib import Path
from typing import List
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA

DB_DIR = "rag_db"
MODEL_NAME = "llama3.1"

embeddings = OllamaEmbeddings(model=MODEL_NAME)
llm = ChatOllama(model=MODEL_NAME, temperature=0.2, timeout=120)


# ---------- Prompt ----------
RAG_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a professional nutrition AI assistant.

Rules:
1. Answer ONLY using the information in the context.
2. Answer in the SAME LANGUAGE as the user's question.
3. Do NOT translate or explain translations.
4. Do NOT mention the context itself.
5. If the answer is not explicitly stated in the context, say:
"I don't know based on the provided documents."
(in the same language as the question)

Context:
{context}

Question:
{question}

Answer:
"""
)





# ---------- Utils ----------
def _db_exists() -> bool:
    return Path(DB_DIR).exists() and any(Path(DB_DIR).iterdir())


def _split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=250,
        chunk_overlap=40,
    )
    return splitter.split_documents(docs)


# ---------- Ingest ----------
def build_vector_store_from_file(path: str) -> int:
    if path.endswith(".txt"):
        loader = TextLoader(path, encoding="utf-8")
    elif path.endswith(".pdf"):
        loader = PyPDFLoader(path)
    else:
        raise ValueError("Only .txt or .pdf supported")

    docs = loader.load()
    chunks = _split_docs(docs)

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR,
    )
    vectordb.persist()
    return len(chunks)


# ---------- Retrieval ----------
def retrieve_docs(query: str):
    if not _db_exists():
        return []

    vectordb = Chroma(
        embedding_function=embeddings,
        persist_directory=DB_DIR,
    )

    retriever = vectordb.as_retriever(search_kwargs={"k": 10})
    docs = retriever.invoke(query)

    # 🔍 DEBUG
    print("\n🔍 Retrieval Debug")
    print(f"Query: {query}")
    for i, doc in enumerate(docs, 1):
        print(f"\nChunk {i}")
        print(doc.page_content[:200])

    return docs


# ---------- RAG ----------
def run_rag(question: str) -> str:
    vectordb = Chroma(
        embedding_function=embeddings,
        persist_directory=DB_DIR,
    )

    retriever = vectordb.as_retriever(search_kwargs={"k": 10})
    docs = retriever.invoke(question)

    print("\n🔍 RUN_RAG DEBUG")
    for i, doc in enumerate(docs, 1):
        print(f"\nChunk {i}")
        print(doc.page_content[:300])

    context = "\n\n".join(doc.page_content for doc in docs)

    chain = LLMChain(
        llm=llm,
        prompt=RAG_PROMPT,
    )

    return chain.run(
        context=context,
        question=question,
    )
