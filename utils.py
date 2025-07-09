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


class PubMedArticleData(dict):

    def __init__(self, **kwargs):
        super().__init__({
            "PMID": None,
            "Title": None,
            "PublicationDate": None,
            "NonAcademicAuthors": set(),
            "CompanyAffiliations": set(),
            "CorrespondingAuthorEmail": None,
        })

        # Allow overrides via kwargs
        for key, value in kwargs.items():
            if key in self:
                self[key] = value

    def to_dict(self):
        return {
            "PMID": self["PMID"],
            "Title": self["Title"],
            "PublicationDate": self["PublicationDate"],
            "NonAcademicAuthors": ", ".join(self["NonAcademicAuthors"]),
            "CompanyAffiliations": ", ".join(self["CompanyAffiliations"]),
            "CorrespondingAuthorEmail": self["CorrespondingAuthorEmail"],
        }
    

def has_company_affiliation(aff):
    aff_lower = aff.lower()
    return any(keyword in aff_lower for keyword in {"inc", "ltd", "corp", "gmbh", "biotech", "pharma", "llc", "s.a.", "co.", "plc"})

def has_academic_affiliation(aff):
    aff_lower = aff.lower()
    return any(term in aff_lower for term in {"univers", "college", "institute", "hospital", "school"})

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group() if match else None


def parsing_an_article(article) -> PubMedArticleData:
    
    data = PubMedArticleData()
    # PMID
    data["PMID"] = article.findtext(".//PMID")

    # Title
    data["Title"] = article.findtext(".//ArticleTitle")

    # Publication Date
    pub_date = article.find(".//PubMedPubDate")
    if pub_date:
        day = pub_date.findtext("Day") or "00"
        month = pub_date.findtext("Month") or "00"
        year = pub_date.findtext("Year") or "0000"       
        
        data["PublicationDate"] = f"{day}-{month}-{year}"

    # Authors & Affiliations
    for author in article.findall(".//Author"):

        firstname = author.findtext("ForeName") or ""
        lastname = author.findtext("LastName") or ""

        affiliations = [a.text for a in author.findall(".//Affiliation") if a.text]

        for aff in affiliations:
            if not has_academic_affiliation(aff) and (firstname or lastname):
                data["NonAcademicAuthors"].add(firstname + " " + lastname)
            
            if has_company_affiliation(aff):
                data["CompanyAffiliations"].add(aff)

            if not data["CorrespondingAuthorEmail"]: #Will be written only once i,e if one email is stored rest are omitted!
                email = extract_email(aff)
                if email:
                    data["CorrespondingAuthorEmail"] = email

    return data