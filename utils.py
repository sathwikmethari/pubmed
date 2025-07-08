import re, requests
from typing import *


#only checks if email is form something@something.something
def validate_email_syntax(email:str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None


#gets email and api key!
def get_email_and_api(base_url:str) -> tuple[str, None | str]:
    while True:
        email=input("---Enter your email---\n>>  ").strip()
        if validate_email_syntax(email):
            break
        else:
            print("---Enter a valid email address---")
    
    
    while True:
        api_key=input("---Enter API key or Enter 'skip' if not available---\n>>  ").strip().lower()

        if api_key == "skip":
            api_key = None
            break
        
        test_params={
                "db": "pubmed",
                "term": "cancer",
                "retmax": 0,
                "retmode": "json",
                "api_key":api_key
            }
        try:
            # Make a minimal valid test request (e.g. search PubMed with harmless query)
            response = requests.get(base_url, params=test_params, timeout=2)
            response.raise_for_status()

            print("---API key verified!---")
            break

        except requests.exceptions.RequestException as e:
            print("---Invalid API key!!---")
            #print(f"Error occured : {type(e)}")
    return email, api_key