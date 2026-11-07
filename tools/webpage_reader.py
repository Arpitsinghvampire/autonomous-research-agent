import requests
from bs4 import BeautifulSoup

from config import MAX_CONTENT_LENGTH


def extract_webpage_content(url: str):

    try:

        headers = {

            "User-Agent": (
                "Mozilla/5.0 "
                "(compatible; ResearchAgent/1.0)"
            )

        }

        response = requests.get(

            url,

            headers=headers,

            timeout=15

        )

        response.raise_for_status()

        content_type = response.headers.get(
            "Content-Type", ""
        )

        if "text/html" not in content_type.lower():

            return ""

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Remove unnecessary elements

        for element in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside"
        ]):

            element.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        return text[:MAX_CONTENT_LENGTH]

    except requests.RequestException as e:

        print(f"Error extracting webpage: {e}")

        return ""

    except Exception as e:

        print(f"Unexpected extraction error: {e}")

        return ""