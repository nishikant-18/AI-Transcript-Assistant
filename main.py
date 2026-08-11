
from dotenv import load_dotenv

from audio import process_input
from transcriber import transcribe_all
from summerize import summarize, generate_title
from extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions,
)
from rag_engine import build_rag_chain, ask_question


# Load environment variables
load_dotenv()


def run_pipeline(source: str, language: str = "english") -> dict:

    print("\n" + "=" * 60)
    print("STARTING AI VIDEO ASSISTANT")
    print("=" * 60)

    # --------------------------------------------------
    # 1. Process input
    # --------------------------------------------------

    print("\n[1/7] Processing input...")

    chunks = process_input(source)

    print(f"Audio chunks created: {len(chunks)}")

    # --------------------------------------------------
    # 2. Transcription
    # --------------------------------------------------

    print("\n[2/7] Transcribing...")

    transcript = transcribe_all(
        chunks,
        language=language
    )

    print("\nRaw transcription:")
    print(transcript[:300])

    if len(transcript) > 300:
        print("...")

    # --------------------------------------------------
    # 3. Generate title
    # --------------------------------------------------

    print("\n[3/7] Generating title...")

    title = generate_title(transcript)

    # --------------------------------------------------
    # 4. Generate summary
    # --------------------------------------------------

    print("\n[4/7] Generating summary...")

    summary = summarize(transcript)

    # --------------------------------------------------
    # 5. Extract meeting information
    # --------------------------------------------------

    print("\n[5/7] Extracting action items...")

    action_items = extract_action_items(transcript)

    print("\n[6/7] Extracting decisions and questions...")

    decisions = extract_key_decisions(transcript)
    questions = extract_questions(transcript)

    # --------------------------------------------------
    # 6. Build RAG
    # --------------------------------------------------

    print("\n[7/7] Building RAG vector store...")

    rag_chain = build_rag_chain(transcript)

    print("\nAI Video Assistant ready!")

    # --------------------------------------------------
    # Return all results
    # --------------------------------------------------

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_items,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain": rag_chain,
    }


if __name__ == "__main__":

    # --------------------------------------------------
    # CLI entry point
    # --------------------------------------------------

    source = input(
        "\nEnter YouTube URL or local file path: "
    ).strip()

    language = input(
        "Language (english/hinglish): "
    ).strip() or "english"

    result = run_pipeline(
        source,
        language
    )

    # --------------------------------------------------
    # Display results
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("AI VIDEO ASSISTANT RESULTS")
    print("=" * 60)

    print(f"\n📌 TITLE")
    print("-" * 60)
    print(result["title"])

    print(f"\n📋 SUMMARY")
    print("-" * 60)
    print(result["summary"])

    print(f"\n✅ ACTION ITEMS")
    print("-" * 60)
    print(result["action_items"])

    print(f"\n🔑 KEY DECISIONS")
    print("-" * 60)
    print(result["key_decisions"])

    print(f"\n❓ OPEN QUESTIONS")
    print("-" * 60)
    print(result["open_questions"])

    # --------------------------------------------------
    # Phase 2 — Chat with meeting
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("💬 CHAT WITH YOUR MEETING")
    print("=" * 60)

    print("Type 'exit' to quit.\n")

    rag_chain = result["rag_chain"]

    while True:

        question = input("You: ").strip()

        if question.lower() in ["exit", "quit", "q"]:
            print("\n👋 Goodbye!")
            break

        if not question:
            continue

        answer = ask_question(
            rag_chain,
            question
        )

        print(f"\n🤖 Assistant: {answer}\n")
