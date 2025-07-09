import os, requests, queue, time
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

from utils import parsing_an_article
from esearcher import make_esearch_call
from queues import fetch_queue, data_queue, shutdown_event

load_dotenv()


RATE_LIMIT = 10  # per second
RETMAX = 1000

def make_efetch_call__and_parse(worker_id:int, webenv:str, query_key:str, email:str, api_key:str) -> None:
    while not fetch_queue.empty():
        try:
            start = fetch_queue.get(timeout=2)
            params = {
                "db": "pubmed",
                "query_key": query_key,
                "WebEnv": webenv,
                "retstart": start,
                "retmax": RETMAX,
                "retmode": "xml",
                "email": email,
                "api_key": api_key
            }

            res = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi", params=params)
            res.raise_for_status()

            print(f"[EF-Thread-{worker_id}] Fetched records {start}-{start + RETMAX - 1}")
            root = ET.fromstring(res.text)
            articles = root.findall(".//PubmedArticle")

            for article in articles:
                parsed = parsing_an_article(article)
                data_queue.put(parsed)
        
        except Exception as e:
            print(f"[EF-{worker_id}] Error at start={start}: {e}")
        finally:
            fetch_queue.task_done()
            time.sleep(1.0 / RATE_LIMIT)  # To respect NCBI limit


if __name__ == "__main__":
    NCBI_API_KEY = os.getenv("NCBI_API_KEY")
    NCBI_EMAIL = os.getenv("email")
    query = "covid-19 AND 2024[dp] AND humans[MeSH Terms]"
    webenv, query_key = make_esearch_call(query = query, email = NCBI_EMAIL, api_key = NCBI_API_KEY)
    fetch_queue.put(1000)
    make_efetch_call__and_parse(worker_id = 1, webenv = webenv, query_key = query_key, email = NCBI_EMAIL, api_key = NCBI_API_KEY)