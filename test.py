#from audio import process_input
#from transcriber import transcribe_all

#source = "https://www.youtube.com/watch?v=Lg-meK5IU8Q"

#chunks = process_input (source)

#print(transcribe_all(chunks))
"""
import os
from dotenv import load_dotenv
load_dotenv()
from audio import process_input
from transcriber import transcribe_all

print("KEY LOADED:", os.getenv("SARVAM_API_KEY"))
print("CWD:", os.getcwd())
source = "https://www.youtube.com/watch?v=tplWXd_T7YQ"
language = "hinglish" # change to "hinglish" to test Sarvam

chunks = process_input(source)
transcript = transcribe_all(chunks, language=language)

print("\n === TRANSCRIPT === \n")
print(transcript)
"""
"""
from dotenv import load_dotenv

# Load environment variables before importing core modules
load_dotenv()

from audio import process_input
from transcriber import transcribe_all
from summerize import summarize, generate_title
from extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions,
)


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

SOURCE = "https://youtu.be/_Q-e_nczWqM?si=OHqFFUIfvJSL1G77"

# "english"  -> Whisper
# "hinglish" -> Sarvam
LANGUAGE = "english"


# --------------------------------------------------
# 1. PROCESS AUDIO
# --------------------------------------------------

print("\n" + "=" * 60)
print(" PROCESSING INPUT")
print("=" * 60)

chunks = process_input(SOURCE)

print(f"Audio chunks created: {len(chunks)}")


# --------------------------------------------------
# 2. TRANSCRIBE
# --------------------------------------------------

print("\n" + "=" * 60)
print(" TRANSCRIBING")
print("=" * 60)

transcript = transcribe_all(
    chunks,
    language=LANGUAGE
)

print("\nTRANSCRIPT")
print("-" * 60)

if len(transcript) > 1000:
    print(transcript[:1000])
    print("\n... [transcript truncated] ...")
else:
    print(transcript)


# --------------------------------------------------
# 3. GENERATE TITLE
# --------------------------------------------------

print("\n" + "=" * 60)
print(" GENERATING TITLE")
print("=" * 60)

title = generate_title(transcript)

print(f"\nTITLE: {title}")


# --------------------------------------------------
# 4. SUMMARIZE
# --------------------------------------------------

print("\n" + "=" * 60)
print(" GENERATING SUMMARY")
print("=" * 60)

summary = summarize(transcript)

print("\nSUMMARY")
print("-" * 60)
print(summary)


# --------------------------------------------------
# 5. EXTRACT ACTION ITEMS
# --------------------------------------------------

print("\n" + "=" * 60)
print(" EXTRACTING ACTION ITEMS")
print("=" * 60)

action_items = extract_action_items(transcript)

print("\nACTION ITEMS")
print("-" * 60)
print(action_items)


# --------------------------------------------------
# 6. EXTRACT KEY DECISIONS
# --------------------------------------------------

print("\n" + "=" * 60)
print(" EXTRACTING KEY DECISIONS")
print("=" * 60)

decisions = extract_key_decisions(transcript)

print("\nKEY DECISIONS")
print("-" * 60)
print(decisions)


# --------------------------------------------------
# 7. EXTRACT OPEN QUESTIONS
# --------------------------------------------------

print("\n" + "=" * 60)
print(" EXTRACTING OPEN QUESTIONS")
print("=" * 60)

questions = extract_questions(transcript)

print("\nOPEN QUESTIONS")
print("-" * 60)
print(questions)


# --------------------------------------------------
# DONE
# --------------------------------------------------

print("\n" + "=" * 60)
print(" PROCESSING COMPLETE")
print("=" * 60)

"""

#test.py
from dotenv import load_dotenv

from transcriber import transcribe_all
from audio import process_input
from claim_verifier import (
    extract_claims,
    verify_claims,
)

load_dotenv()

source = "https://youtu.be/r-vbm9Hifw0?si=Hrfp29bRfq1_hnKM"

print("=" * 60)
print("TESTING FULL CLAIM VERIFICATION PIPELINE")
print("=" * 60)

# --------------------------------------------------
# 1. Process audio
# --------------------------------------------------

print("\n[1] Processing audio...")

chunks = process_input(source)

print(f"Audio chunks created: {len(chunks)}")


# --------------------------------------------------
# 2. Transcribe
# --------------------------------------------------

print("\n[2] Transcribing...")

transcript = transcribe_all(
    chunks,
    language="english"
)

print("\nTranscription complete.")


# --------------------------------------------------
# 3. Extract factual claims
# --------------------------------------------------

print("\n[3] Extracting factual claims...")

claims_text = extract_claims(transcript)

print("\n" + "=" * 60)
print("FACTUAL CLAIMS")
print("=" * 60)

print(claims_text)


# --------------------------------------------------
# 4. Verify claims using Tavily
# --------------------------------------------------

print("\n[4] Verifying claims using Tavily...")

verification_results = verify_claims(claims_text)


# --------------------------------------------------
# 5. Display verification results
# --------------------------------------------------

print("\n" + "=" * 60)
print("CLAIM VERIFICATION RESULTS")
print("=" * 60)

for i, result in enumerate(verification_results, start=1):

    print(f"\n{'-' * 60}")
    print(f"CLAIM {i}")
    print("-" * 60)

    print(f"\nClaim:")
    print(result["claim"])

    print("\nVerification:")
    print(result["verification"])

    print("\nSources:")

    for j, source in enumerate(result["sources"], start=1):

        print(f"\n  [{j}] {source['title']}")
        print(f"      {source['url']}")
        print(f"      {source['snippet'][:300]}...")


print("\n" + "=" * 60)
print("CLAIM VERIFICATION TEST COMPLETE")
print("=" * 60)