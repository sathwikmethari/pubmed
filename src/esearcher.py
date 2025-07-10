#Gets webenv and query_key(required for fetching details from from the History server)
import requests, time
from typing import Tuple
from src.email_api import get_email_api_query
from src.utils import default_params

def make_esearch_call(query: str, api_key: None | str, email: str = "your_email@example.com") -> Tuple[str, str]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    params = default_params()
    params["term"] = query
    params["usehistory"] ="y"
    params["email"] = email
    params["api_key"] = api_key
    
    query_is_valid = False

    if api_key:
        params["api_key"] = api_key

    try:
        start_time = time.time()
        res = requests.get(url, params=params)
        res.raise_for_status()

        data = res.json()["esearchresult"]

        count = int(data["count"])
        webenv = data["webenv"]
        query_key = data["querykey"]
        query_is_valid = True
        end_time = time.time()
        print(f"Total results: {count}.  Time taken: {end_time - start_time:.4f} sec")
    
    except requests.exceptions.RequestException as e:
        print("Network or Request error")
        return query_is_valid
    
    except ValueError:
        print("Likely invalid query syntax.")
        return query_is_valid
    
    return query_is_valid,count, webenv, query_key

if __name__ == "__main__":
    email, api_key, query=get_email_api_query(base_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi")
    #query = "covid-19 AND 2024[dp] AND humans[MeSH Terms]"
    query_is_valid, count, webenv, query_key = make_esearch_call(query = query, email=email, api_key=api_key)
