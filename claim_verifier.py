#claim_verifier.py
import os
import re
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tavily import TavilyClient


def get_llm():
    return ChatOllama(
        model=os.getenv("OLLAMA_MODEL", "qwen3:4b"),
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        temperature=0.1,
    )


def get_tavily_client():
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY environment variable is missing.")
    return TavilyClient(api_key=api_key)


def extract_claims(transcript: str) -> str:
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are an expert fact-checking claim extraction assistant.

Your task is to identify ONLY meaningful, externally verifiable factual claims from the transcript.
No subjective or personal life related claims, it should be universe related claims that can be verified from an external source.
A claim should describe something that could reasonably be checked against an authoritative external source.

GOOD CLAIMS include:
- Historical events
- Dates
- Statistics
- Numbers
- Scientific or technical statements
- Company actions or announcements
- Product specifications
- Government policies
- Military or organizational procedures
- Statements about real-world events
- Research findings
- Specific measurable outcomes

DO NOT extract:
- Opinions
- Advice
- Life lessons
- Motivational statements
- Predictions
- Hypothetical examples
- Rhetorical statements
- Metaphors
- Philosophical statements
- Personal beliefs
- Statements such as "you should..."
- Statements such as "life is..."
- Statements about what someone thinks or feels
- Generic statements that cannot be independently verified

IMPORTANT:
Do NOT convert advice or opinions into factual claims.

Only extract claims that are sufficiently specific to be independently checked.

For each claim:
1. Write ONE concise standalone factual statement.
2. Preserve the original meaning.
3. Do not add information that is not explicitly stated.
4. Do not exaggerate the claim.

Return ONLY the numbered claims.

Do NOT provide:
- rationale
- explanations
- analysis
- justification
- categories
- commentary

Correct output format:
1. The speaker served in the Navy SEALs for 36 years.
2. SEAL training requires recruits to make their beds every morning.

If no meaningful claims are found, return exactly:
No verifiable factual claims found.
"""
        ),
        ("human", "{transcript}")
    ])

    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"transcript": transcript})


def parse_claims(claims_text: str) -> list[str]:
    if "no verifiable factual claims found" in claims_text.lower():
        print("\n[INFO] No factual claims were detected in the transcript.")
        return []
    claims = []
    # Matches lines starting with "1. ", "2) ", etc.
    claim_pattern = re.compile(r"^\d+[\.\)]\s*(.+)$")

    for line in claims_text.splitlines():
        line = line.strip()
        match = claim_pattern.match(line)
        if match:
            claims.append(match.group(1).strip())

    return claims


def search_claim(claim: str) -> list[dict]:
    tavily = get_tavily_client()
    response = tavily.search(
        query=claim,
        search_depth="advanced",
        max_results=5,
        include_answer=False,
        include_raw_content=False,
    )
    return response.get("results", [])


def verify_claim(claim: str) -> dict:

    print(f"\nVerifying claim: {claim}")

    # --------------------------------------------------
    # 1. Search claim using Tavily
    # --------------------------------------------------

    results = search_claim(claim)

    if not results:
        return {
            "claim": claim,
            "verification": (
                "VERDICT: UNVERIFIED\n"
                "CONFIDENCE: LOW\n"
                "EXPLANATION: No relevant external sources were found.\n"
                "EVIDENCE: No external evidence available."
            ),
            "sources": []
        }

    # --------------------------------------------------
    # 2. Prepare external evidence
    # --------------------------------------------------

    evidence_parts = []

    for i, result in enumerate(results, start=1):

        title = result.get("title", "")
        url = result.get("url", "")
        content = result.get("content", "")

        evidence_parts.append(
            f"""
SOURCE {i}
TITLE: {title}
URL: {url}
CONTENT: {content}
"""
        )

    evidence = "\n".join(evidence_parts)

    # --------------------------------------------------
    # 3. Ask Qwen to verify
    # --------------------------------------------------

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are an expert fact-checking assistant.

Verify the factual claim using ONLY the external sources
provided below.

Do NOT use your own knowledge.

Classify the claim into exactly one category:

VERIFIED
PARTIALLY VERIFIED
CONTRADICTED
UNVERIFIED

Definitions:

VERIFIED:
Reliable external evidence directly supports the main claim.

PARTIALLY VERIFIED:
Evidence supports part of the claim, but some details are
missing, uncertain, exaggerated, or different.

CONTRADICTED:
Reliable external evidence directly conflicts with the claim.

UNVERIFIED:
The available sources do not provide enough reliable evidence
to determine whether the claim is true.

Important:

- Do not assume the claim is true.
- Do not trust a source merely because it appears in search results.
- Compare the actual evidence with the claim.
- Pay attention to dates, numbers, names, and specific details.
- Prefer authoritative sources when available.
- If sources disagree, mention the disagreement.
- Do not use outside knowledge.

Return exactly:

VERDICT: <VERIFIED | PARTIALLY VERIFIED | CONTRADICTED | UNVERIFIED>

CONFIDENCE: <HIGH | MEDIUM | LOW>

EXPLANATION:
<2-4 concise sentences>

EVIDENCE:
<the most relevant evidence from the sources>
"""
        ),
        (
            "human",
            """
CLAIM:
{claim}

EXTERNAL SOURCES:
{evidence}
"""
        )
    ])

    chain = prompt | llm | StrOutputParser()

    raw_verification = chain.invoke({
        "claim": claim,
        "evidence": evidence
    })

    # --------------------------------------------------
    # 4. Return structured result
    # --------------------------------------------------

    return {
        "claim": claim,
        "verification": raw_verification,
        "sources": [
            {
                "title": result.get("title"),
                "url": result.get("url"),
                "snippet": result.get("content")
            }
            for result in results
        ]
    }


def verify_claims(claims_text: str) -> list:
    claims = parse_claims(claims_text)
    results = []

    for claim in claims:
        result = verify_claim(claim)
        results.append(result)

    return results