
# extractor.py
# Actionable Items, Key Decisions, Questions

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
import os


def get_llm():
    return ChatOllama(
        model=os.getenv("OLLAMA_MODEL", "qwen3:4b"),
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        temperature=0.2
    )


def build_chain(system_prompt: str):
    llm = get_llm()

    return (
        RunnablePassthrough()
        | RunnableLambda(lambda x: {"text": x})
        | ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{text}"),
        ])
        | llm
        | StrOutputParser()
    )


def extract_action_items(transcript: str) -> str:
    chain = build_chain(
        "You are an expert meeting analyst. "
        "From the meeting transcript, extract all action items. "
        "For each action item provide:\n"
        "- Task description\n"
        "- Owner (who is responsible)\n"
        "- Deadline (if mentioned, otherwise write 'Not specified')\n\n"
        "Format the result as a numbered list. "
        "Do not invent information that is not present in the transcript. "
        "If no action items are found, say 'No action items found.'"
    )

    return chain.invoke(transcript)


def extract_key_decisions(transcript: str) -> str:
    chain = build_chain(
        "You are an expert meeting analyst. "
        "From the meeting transcript, extract all key decisions that were "
        "actually made during the meeting.\n\n"
        "Do not include suggestions or unresolved discussions as decisions. "
        "Do not invent information.\n\n"
        "Format the result as a numbered list. "
        "If no key decisions are found, say 'No key decisions found.'"
    )

    return chain.invoke(transcript)


def extract_questions(transcript: str) -> str:
    chain = build_chain(
        "You are an expert meeting analyst. "
        "From the meeting transcript, extract all unresolved questions "
        "or topics that require follow-up.\n\n"
        "Do not include questions that were already answered. "
        "Do not invent information.\n\n"
        "Format the result as a numbered list. "
        "If no unresolved questions are found, say 'No open questions found.'"
        "Return only the numbered list. "
        "Do not explain your reasoning."
    )

    return chain.invoke(transcript)
