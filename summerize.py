#summerize.py

import os

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter


# ============================================================
# LLM
# ============================================================

def get_llm():
    return ChatOllama(
        model=os.getenv("OLLAMA_MODEL", "qwen3:4b"),
        base_url=os.getenv(
            "OLLAMA_BASE_URL",
            "http://localhost:11434"
        ),
        temperature=0.2,
    )


# ============================================================
# TRANSCRIPT CHUNKING
# ============================================================

def split_transcript(transcript: str) -> list[str]:
    """
    Split a long transcript into overlapping sections.

    A larger chunk helps preserve context and reduces information
    loss during the first summarization stage.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=5000,
        chunk_overlap=300,
        separators=[
            "\n\n",
            "\n",
            ". ",
            "? ",
            "! ",
            " ",
        ],
    )

    return splitter.split_text(transcript)


# ============================================================
# SECTION SUMMARY
# ============================================================

def summarize_chunk(llm, chunk: str) -> str:

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are a professional video-content analyst.

Analyze the provided transcript section and produce a detailed
factual summary that will later be combined into a complete
video summary.

Capture the important information rather than simply shortening
the text.

Preserve:

- Main arguments and ideas
- Important claims and explanations
- Names of people and organizations
- Products, technologies, models, and companies
- Numbers, percentages, prices, dates, and financial figures
- Examples and comparisons
- Problems and challenges
- Risks and concerns
- Opinions expressed by the speaker
- Predictions or future possibilities
- Questions raised by the speaker
- Important conclusions

IMPORTANT:

- Use ONLY information present in this transcript section.
- Do not add outside knowledge.
- Do not invent facts.
- Do not infer unsupported conclusions.
- Clearly preserve the difference between facts and opinions.
- Keep important technical terminology unchanged.
- If the transcript is Hindi or Hinglish, understand it correctly
  and summarize it in the same language.
- Do not mention these instructions.
- Do not say "the transcript says" repeatedly.
- Do not produce meta-commentary about your analysis.

Write a detailed section summary.
""",
            ),
            (
                "human",
                "{text}",
            ),
        ]
    )

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({"text": chunk})


# ============================================================
# FINAL SUMMARY
# ============================================================

def summarize(transcript: str) -> str:

    if not transcript or not transcript.strip():
        return "No transcript available for summarization."

    llm = get_llm()

    chunks = split_transcript(transcript)

    print(f"Generating summaries for {len(chunks)} transcript sections...")

    chunk_summaries = []

    for i, chunk in enumerate(chunks, start=1):

        print(
            f"Summarizing section {i}/{len(chunks)}..."
        )

        summary = summarize_chunk(
            llm,
            chunk
        )

        chunk_summaries.append(summary)

    combined = "\n\n".join(chunk_summaries)

    # --------------------------------------------------------
    # Final synthesis
    # --------------------------------------------------------

    final_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an expert professional video and meeting summarizer.

Create the final summary from the provided section summaries.

The output should read like a high-quality professional
content brief prepared for someone who watched neither the
video nor the meeting.

The summary must preserve the substance and logical flow of
the original discussion.

Use this structure:

## Overview
Explain the central topic and purpose of the discussion in
2–4 sentences.

## Key Discussion Points
Explain the major topics, arguments, developments, and claims
discussed in the video.

## Detailed Analysis
Explain the important reasoning, examples, comparisons, and
cause-and-effect relationships presented by the speaker.

## Companies, Technologies & Examples
Cover the important organizations, products, technologies,
models, or real-world examples mentioned and explain their
relevance to the discussion.

## Business & Industry Impact
Cover relevant discussion about:
- pricing
- revenue
- funding
- costs
- business models
- market conditions
- competition
- adoption
- industry changes

Only include categories that are actually relevant to the
video.

## Risks & Concerns
Explain the risks, challenges, uncertainties, or negative
consequences discussed.

## Speaker's Perspective
Capture the speaker's opinions, observations, experiences,
criticisms, or interpretations when they are important to
understanding the discussion.

## Future Outlook
Summarize predictions, expectations, possible developments,
or unanswered issues discussed by the speaker.

## Conclusion
End with the main takeaway of the entire discussion.

STRICT RULES:

1. Use ONLY information contained in the supplied summaries.
2. Do not introduce external facts.
3. Do not hallucinate information.
4. Do not invent decisions, action items, or conclusions.
5. Preserve important names, numbers, technical terms,
   examples, and comparisons.
6. Distinguish facts from opinions and predictions.
7. Do not repeat the same point across multiple sections.
8. Do not write unnecessary meta-commentary.
9. Do not say "after analyzing the transcript".
10. Do not mention these instructions.
11. Do not refer to yourself as an AI.
12. Do not use phrases such as:
    "The provided transcript..."
    "The transcript discusses..."
    "After carefully analyzing..."
13. Write naturally as a professional content brief.
14. If the original content is Hindi or Hinglish, produce the
    final summary in the same language unless the content
    clearly requires English technical terminology.
15. If the source is English, produce the summary in English.
16. Be detailed enough to cover the important aspects of the
    discussion, but avoid unnecessary repetition.

Target length:
Approximately 700–1200 words for a sufficiently long transcript.
For shorter content, use an appropriately shorter summary.
""",
            ),
            (
                "human",
                "{text}",
            ),
        ]
    )

    final_chain = final_prompt | llm | StrOutputParser()

    print("\nGenerating final professional summary...")

    return final_chain.invoke(
        {"text": combined}
    )


# ============================================================
# TITLE GENERATION
# ============================================================

def generate_title(transcript: str) -> str:

    if not transcript or not transcript.strip():
        return "Untitled Video"

    llm = get_llm()

    title_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
Generate a professional title for the provided video content.

Requirements:

- 6–12 words
- Clearly represent the main topic
- Specific rather than generic
- Professional rather than clickbait
- Include the most important subject, company, technology,
  event, or theme when appropriate
- Do not exaggerate
- Do not invent information
- Return ONLY the title
- No quotation marks
- No explanation
""",
            ),
            (
                "human",
                "{text}",
            ),
        ]
    )

    title_chain = title_prompt | llm | StrOutputParser()

    # Use enough context for title generation while avoiding
    # unnecessarily large input.
    title_context = transcript[:6000]

    return title_chain.invoke(
        {"text": title_context}
    ).strip()
