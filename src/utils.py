import re, requests
from typing import *


#only checks if email is form something@something.something
def validate_email_syntax(email:str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

#Dictionary class with default params
class default_params(dict):

    def __init__(self, **kwargs):
        super().__init__({
            "db": "pubmed",
            "retstart": 0,
            "retmax": 0,
            "retmode": "json",
            "email": None,
            "api_key": None,
        })

        # Allow overrides via kwargs
        for key, value in kwargs.items():
            if key in self:
                self[key] = value

    def to_dict(self):
        return {
            "db": self["db"],
            "retstart": self["retstart"],
            "retmax": self["retmax"],
            "retmode":self["retmode"],
            "email": self["email"],
            "api_key": self["api_key"],
        }

#Dictionary class to store PMID details
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
    #Initiliazing a created class object
    data = PubMedArticleData()
    # PMID
    data["PMID"] = article.findtext(".//PMID")

    # Title
    data["Title"] = article.findtext(".//ArticleTitle")

    # Publication Date(if any of day/month/year is not available add zeros instead)
    pub_date = article.find(".//PubMedPubDate")
    if pub_date:
        day = pub_date.findtext("Day") or "00"
        month = pub_date.findtext("Month") or "00"
        year = pub_date.findtext("Year") or "0000"       
        
        data["PublicationDate"] = f"{day}-{month}-{year}"

    # Authors & Affiliations
    # Loop through all authors
    for author in article.findall(".//Author"):

        firstname = author.findtext("ForeName") or ""
        lastname = author.findtext("LastName") or ""

        affiliations = [a.text for a in author.findall(".//Affiliation") if a.text]

        # Loop through all affiliations
        for aff in affiliations:
            #If there are no academic affiliations add to the Dictionary
            if not has_academic_affiliation(aff) and (firstname or lastname):
                data["NonAcademicAuthors"].add(firstname + " " + lastname)

            #If there are company academic affiliations add to the Dictionary
            if has_company_affiliation(aff):
                data["CompanyAffiliations"].add(aff)

            #add email only once i,e if one email is stored rest are omitted!
            if not data["CorrespondingAuthorEmail"]: 
                email = extract_email(aff)
                if email:
                    data["CorrespondingAuthorEmail"] = email
    return data