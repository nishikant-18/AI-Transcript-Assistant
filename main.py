"""
from dotenv import load_dotenv

from audio import process_input
from transcriber import transcribe_all
from summerize import summarize, generate_title
from claim_verifier import extract_claims, verify_claim, verify_claims
from extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions
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
    print("\n[8/8] Extracting factual claims...")

    claims = extract_claims(transcript)

    print("\n[9/9] Verifying factual claims...")

    verified_claims = verify_claims(claims)
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
        "claims": claims,
        "verified_claims": verified_claims,
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
    print("\n🔎 FACT CHECK")
    print("-" * 60)

    print("\nExtracted Claims:")
    print(result["claims"])

    print("\nVerification Results:")

    for i, result_item in enumerate(
        result["verified_claims"],
        start=1
    ):
        print(f"\nClaim {i}")
        print("-" * 60)

        print(result_item["claim"])

        print("\nVerification:")
        print(result_item["verification"])

        print("\nSources:")

        for source in result_item["sources"]:
            print(f"- {source['title']}")
            print(f"  {source['url']}")
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
"""





from dotenv import load_dotenv

from audio import process_input
from transcriber import transcribe_all
from summerize import summarize, generate_title

from claim_verifier import (
    extract_claims,
    verify_claims
)

from extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions
)

from rag_engine import (
    build_rag_chain,
    ask_question
)


# Load environment variables
load_dotenv()


def run_pipeline(source: str, language: str = "english") -> dict:

    print("\n" + "=" * 60)
    print("STARTING AI VIDEO ASSISTANT")
    print("=" * 60)

    # --------------------------------------------------
    # 1. Process input
    # --------------------------------------------------

    print("\n[1/9] Processing input...")

    chunks = process_input(source)

    print(f"Audio chunks created: {len(chunks)}")

    # --------------------------------------------------
    # 2. Transcription
    # --------------------------------------------------

    print("\n[2/9] Transcribing...")

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

    print("\n[3/9] Generating title...")

    title = generate_title(transcript)

    # --------------------------------------------------
    # 4. Generate summary
    # --------------------------------------------------

    print("\n[4/9] Generating summary...")

    summary = summarize(transcript)

    # --------------------------------------------------
    # 5. Extract meeting information
    # --------------------------------------------------

    print("\n[5/9] Extracting action items...")

    action_items = extract_action_items(transcript)

    print("\n[6/9] Extracting decisions and questions...")

    decisions = extract_key_decisions(transcript)
    questions = extract_questions(transcript)

    # --------------------------------------------------
    # 6. Build RAG
    # --------------------------------------------------

    print("\n[7/9] Building RAG vector store...")

    rag_chain = build_rag_chain(transcript)

    # --------------------------------------------------
    # 7. Extract factual claims
    # --------------------------------------------------

    print("\n[8/9] Extracting factual claims...")

    claims = extract_claims(transcript)

    # --------------------------------------------------
    # 8. Verify factual claims
    # --------------------------------------------------

    print("\n[9/9] Verifying factual claims using Tavily...")

    verified_claims = verify_claims(claims)

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

        # Claim verification
        "claims": claims,
        "verified_claims": verified_claims,

        # RAG
        "rag_chain": rag_chain,
    }


# ======================================================
# CLI
# ======================================================

if __name__ == "__main__":

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

    # ==================================================
    # DISPLAY RESULTS
    # ==================================================

    print("\n" + "=" * 60)
    print("AI VIDEO ASSISTANT RESULTS")
    print("=" * 60)

    # --------------------------------------------------
    # TITLE
    # --------------------------------------------------

    print("\n📌 TITLE")
    print("-" * 60)

    print(result["title"])

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    print("\n📋 SUMMARY")
    print("-" * 60)

    print(result["summary"])

    # --------------------------------------------------
    # ACTION ITEMS
    # --------------------------------------------------

    print("\n✅ ACTION ITEMS")
    print("-" * 60)

    print(result["action_items"])

    # --------------------------------------------------
    # KEY DECISIONS
    # --------------------------------------------------

    print("\n🔑 KEY DECISIONS")
    print("-" * 60)

    print(result["key_decisions"])

    # --------------------------------------------------
    # OPEN QUESTIONS
    # --------------------------------------------------

    print("\n❓ OPEN QUESTIONS")
    print("-" * 60)

    print(result["open_questions"])

    # ==================================================
    # FACT CHECK
    # ==================================================

    print("\n" + "=" * 60)
    print("🔎 FACTUAL CLAIM VERIFICATION")
    print("=" * 60)

    # --------------------------------------------------
    # EXTRACTED CLAIMS
    # --------------------------------------------------

    print("\n📌 EXTRACTED CLAIMS")
    print("-" * 60)

    print(result["claims"])

    # --------------------------------------------------
    # VERIFICATION RESULTS
    # --------------------------------------------------

    print("\n📊 VERIFICATION RESULTS")
    print("-" * 60)

    for i, claim_result in enumerate(
        result["verified_claims"],
        start=1
    ):

        print(f"\nCLAIM {i}")
        print("-" * 60)

        print(f"Claim:")
        print(claim_result["claim"])

        print("\nVerification:")
        print(claim_result["verification"])

        print("\nSources:")

        for j, source in enumerate(
            claim_result["sources"],
            start=1
        ):

            print(f"\n  [{j}] {source['title']}")
            print(f"      {source['url']}")

    # ==================================================
    # CHAT WITH MEETING
    # ==================================================

    print("\n" + "=" * 60)
    print("💬 CHAT WITH YOUR MEETING")
    print("=" * 60)

    print("Type 'exit' to quit.\n")

    rag_chain = result["rag_chain"]

    while True:

        question = input("You: ").strip()

        if question.lower() in [
            "exit",
            "quit",
            "q"
        ]:

            print("\n👋 Goodbye!")
            break

        if not question:
            continue

        answer = ask_question(
            rag_chain,
            question
        )

        print(f"\n🤖 Assistant: {answer}\n")