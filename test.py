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

