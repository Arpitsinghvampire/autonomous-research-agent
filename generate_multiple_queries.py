import json
import re

from langchain_ollama import ChatOllama

from config import (
    OLLAMA_MODEL,
    OLLAMA_BASE_URL,
    MAX_SEARCH_QUERIES
)


llm = ChatOllama(

    model=OLLAMA_MODEL,

    base_url=OLLAMA_BASE_URL,

    temperature=0

)


def generate_search_queries(question: str):

    prompt = f"""
You are an expert research assistant.

Your task is to decompose a research question
into focused search queries.

Research question:
{question}

Generate exactly {MAX_SEARCH_QUERIES} distinct
search queries.

Rules:
1. Each query must explore a different aspect.
2. Keep queries specific and meaningful.
3. Avoid duplicate queries.
4. Do not answer the research question.
5. Return only valid JSON.

Required format:

{{
    "queries": [
        "query 1",
        "query 2",
        "query 3",
        "query 4"
    ]
}}
"""

    try:

        response = llm.invoke(prompt)

        content = response.content

        # Extract JSON in case the model adds
        # markdown code fences.

        match = re.search(
            r"\{.*\}",
            content,
            re.DOTALL
        )

        if not match:

            raise ValueError(
                "No JSON object returned by model"
            )

        data = json.loads(match.group())

        queries = data.get("queries", [])

        queries = [
            q.strip()
            for q in queries
            if isinstance(q, str) and q.strip()
        ]

        # Remove duplicate queries

        queries = list(dict.fromkeys(queries))

        if not queries:

            raise ValueError(
                "No valid queries generated"
            )

        return queries[:MAX_SEARCH_QUERIES]

    except Exception as e:

        print(f"Query generation error: {e}")

        # Fallback: use original question

        return [question]