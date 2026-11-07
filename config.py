import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "gemma3:270m"
)

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)

MAX_SEARCH_QUERIES = 4

MAX_WEB_RESULTS = 5

MAX_ARXIV_RESULTS = 5

MAX_CONTENT_LENGTH = 10000