#Gets webenv and query_key(required for fetching details from from the History server)
import requests, os
from typing import Tuple
from dotenv import load_dotenv

load_dotenv()


def make_esearch_call(query: str, api_key: None | str, email: str = "your_email@example.com") -> Tuple[str, str]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    params = {
        "db": "pubmed",
        "term": query,
        "usehistory": "y",
        "retmode": "json",
        "retmax": 0,
        "email": email
    }

    if api_key:
        params["api_key"] = api_key

    res = requests.get(url, params=params)
    res.raise_for_status()

    data = res.json()["esearchresult"]

    count = int(data["count"])
    webenv = data["webenv"]
    query_key = data["querykey"]

    print(f"Total results: {count}")
    
    return webenv, query_key

if __name__ == "__main__":
    NCBI_EMAIL = os.getenv("NCBI_API_KEY")
    NCBI_API_KEY = os.getenv("email")
    query = "covid-19 AND 2024[dp] AND humans[MeSH Terms]"
    webenv, query_key = make_esearch_call(query, NCBI_EMAIL,NCBI_API_KEY)
    #print(webenv, query_key)
