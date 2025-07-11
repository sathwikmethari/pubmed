#gets email, api key and query!
import requests, getpass
from src.utils import validate_email_syntax, validate_query

def get_email_api_query(base_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi") -> tuple[str, None | str, str]:
    while True:
        email=input("Enter your email\n>>  ").strip()
        if validate_email_syntax(email):
            break
        else:
            print("Enter a valid email address")    
    
    while True:
        api_key=getpass.getpass("Enter API key or 'skip'\n>>  ").strip().lower()

        if api_key == "skip":
            api_key = None
            break
        
        test_params = {
        "db": "pubmed",
        "retmode": "json",
        "retmax": 0,
        "email" : email,
        "api_key": api_key
        }

        try:
            # Make a minimal valid test request (e.g. search PubMed with harmless query)
            response = requests.get(base_url, params=test_params, timeout=2)
            response.raise_for_status()

            print("API key verified!")
            break

        except requests.exceptions.RequestException as e:
            print("Invalid API key!!")
            #print(f"Error occured : {type(e)}")
    while True:
        query = input("Enter your query\n>>  ")
        if validate_query(query):
            break
        else:
            print("Invalid query!\n")
    return email, api_key, query

if __name__ == "__main__":
    email, api_key, query = get_email_api_query()