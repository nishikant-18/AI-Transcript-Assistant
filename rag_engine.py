
import os

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from vector_store import (
    build_vector_store,
    load_vector_store,
    get_retriever,
)


def get_llm():
    return ChatOllama(
        model=os.getenv("OLLAMA_MODEL", "qwen3:4b"),
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        temperature=0.3,
    )


def format_docs(docs):
    return "\n\n".join(
        [doc.page_content for doc in docs]
    )


def build_rag_chain(transcript: str):

    # Build vector store from transcript
    vector_store = build_vector_store(transcript)

    # Create retriever
    retriever = get_retriever(
        vector_store,
        k=4
    )

    # Local Ollama LLM
    llm = get_llm()

    # RAG prompt
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are an expert meeting assistant.

Answer the user's question based ONLY on the meeting transcript
context provided below.

If the answer is not found in the context, say exactly:

"I could not find this information in the meeting transcript."

Do not use outside knowledge.
Do not make assumptions.
Do not invent information.

Always be concise and precise.

If quoting someone, clearly indicate that it is a quote.

Context from meeting transcript:
{context}"""
        ),
        (
            "human",
            "{question}"
        ),
    ])

    # Full LCEL RAG pipeline
    rag_chain = (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


def load_rag_chain():

    # Load existing vector store
    vector_store = load_vector_store()

    # Create retriever from vector store
    retriever = get_retriever(
        vector_store,
        k=4
    )

    # Local Ollama LLM
    llm = get_llm()

    # RAG prompt
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are an expert meeting and video analysis assistant.

Answer the user's question using ONLY the provided transcript
context.

Follow these rules:

1. Use information explicitly present in the transcript.
2. You may connect information from different parts of the
   transcript when the connection is directly supported.
3. Do NOT introduce outside knowledge.
4. Do NOT speculate beyond what the speaker discussed.
5. Clearly distinguish between:
   - Facts mentioned in the transcript
   - The speaker's opinions
   - Predictions or possibilities
6. If the question is only partially answered by the transcript,
   explain what information IS available and clearly state what
   is not available.
7. If the topic is completely absent, say:

"I could not find this information in the meeting transcript."

8. When useful, mention the relevant company, technology,
   example, or argument from the transcript.
9. Provide a detailed but focused answer rather than a one-line
   response.

For questions asking about future risks or threats, do not
invent a threat. Instead explain the risks that the speaker
actually discussed and state whether the specific question was
addressed.

Context from meeting transcript:
{context}

"""
        ),
        (
            "human",
            "{question}"
        ),
    ])

    rag_chain = (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


def ask_question(rag_chain, question: str) -> str:

    print(f"\nQuestion: {question}")

    answer = rag_chain.invoke(question)

    print(f"\nAnswer: {answer}")

    return answer

