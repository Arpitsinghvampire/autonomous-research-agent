import json  
import os  
import streamlit as st 
from datetime import datetime  

from get_consistent_structure import ResearchSource , ResearchOutput  
from generate_multiple_queries import generate_search_queries 
from tools.arxiv import search_arxiv  

from tools.duckduckgo import search_web  

from tools.webpage_reader import extract_webpage_content

from config import (MAX_WEB_RESULTS , MAX_ARXIV_RESULTS)

def run_research(question: str):

    # Step 1: Generate search queries
    queries = generate_search_queries(question)

    all_results = []

    # Step 2: Search the web and arXiv
    for query in queries:

        web_results = search_web(
            query,
            max_results=MAX_WEB_RESULTS
        )

        all_results.extend(web_results)

        # Search arXiv
        arxiv_results = search_arxiv(
            query,
            max_results=MAX_ARXIV_RESULTS
        )

        all_results.extend(arxiv_results)

    # Step 3: Remove duplicate sources
    unique_results = {}

    for result in all_results:

        url = result.get("url")

        if url and url not in unique_results:
            unique_results[url] = result

    all_results = list(unique_results.values())

    # Step 4: Process and structure sources
    structured_sources = []

    for index, result in enumerate(all_results):

        content = result.get("snippet", "")

        if result["source_type"] == "web":

            extracted_content = extract_webpage_content(
                result["url"]
            )

            if extracted_content:
                content = extracted_content

        source = ResearchSource(

            title=result.get("title", ""),

            url=result["url"],

            source_type=result["source_type"],

            snippet=result.get("snippet", ""),

            content=content,

            authors=result.get("authors", []),

            published_date=result.get("published_date")

        )

        structured_sources.append(source)

    # Step 5: Create final research output
    research_output = ResearchOutput(

        original_question=question,

        search_queries=queries,

        sources=structured_sources,

        total_sources=len(structured_sources)

    )

    return research_output

st.title("AUTONOMOUS RESEARCH AGENT")

query = st.text_area("Enter the query .... " ,placeholder = "Application of Graph Neural networks in healthcare")

#after getting the query 

if st.button("Start Research"):

	if query.strip():

		with st.spinner("Fetching results ....Please wait"):

			result = run_research(query)

			for res in result.sources :

				st.subheader(res.title)
				st.write(res.content)
				st.write(res.url)
				st.divider()

		st.success("Research Completed")






