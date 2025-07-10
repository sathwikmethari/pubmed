import requests, time, yaml
import xml.etree.ElementTree as ET

from src.email_api import get_email_api_query
from src.esearcher import make_esearch_call
from src.utils import parsing_an_article, default_params
from src.queues import fetch_queue, data_queue

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

rate_limit = config["ncbi"]["rate_limit"]  # per second
retmax = config["ncbi"]["retmax"]  

def make_efetch_call__and_parse(worker_id:int, webenv:str, query_key:str, email:str, api_key:str) -> None:
    while not fetch_queue.empty():
        try:
            start = fetch_queue.get(timeout=2)
            params = {
                "db": "pubmed",
                "query_key": query_key,
                "WebEnv": webenv,
                "retstart": start,
                "retmax": retmax,
                "retmode": "xml",
                "email": email,
                "api_key": api_key
            }
            
            start_time = time.time()
            res = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi", params=params)
            res.raise_for_status()
            end_time = time.time()

            print(f"[EF-Thread-{worker_id}] Fetched records {start}-{start + retmax - 1}. Time taken: {end_time - start_time:.4f} sec")
            root = ET.fromstring(res.text)
            articles = root.findall(".//PubmedArticle")

            for article in articles:
                parsed = parsing_an_article(article)
                data_queue.put(parsed)
        
        except Exception as e:
            print(f"[EF-{worker_id}] Error at start={start}: {e}")
        finally:
            fetch_queue.task_done()
            time.sleep(1.0 / rate_limit)  # To respect NCBI limit


if __name__ == "__main__":
    email, api_key, query = get_email_api_query(base_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi")
    query = "covid-19 AND 2024[dp] AND humans[MeSH Terms]"
    query_is_valid, count, webenv, query_key = make_esearch_call(query = query, email=email, api_key=api_key)
    if query_is_valid:
        fetch_queue.put(1000)
        #make_efetch_call__and_parse(worker_id = 1, webenv = webenv, query_key = query_key, email = email, api_key = api_key)