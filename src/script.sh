#!/bin/bash

echo "**** Available commands ****
|-------------------------------------------------|
| run          | Runs the main file.              |
| -h or --help | Display usage instructions.      |
| -f or --file | Specify the filename.            |
| exit         | exits the Code                   |
|-------------------------------------------------|
"
while true; do
read -p ">> " input
if [[ "$input" == "run" ]]; then
    echo "Running Python script..."
    python3 example.py
elif [[ "$input" == "-h" || "$input" == "--help" ]]; then
    echo -e "
    -- start of page --

    **** PubMed supports Boolean operators ****
    |---------------------------------------|
    | operator| example                     |
    |---------------------------------------|
    | AND     | cancer AND tumor            |
    | OR      | cancer OR tumor             |
    | NOT     | immunotherapy NOT vaccines  |
    |---------------------------------------|

    **** You can attach tags in square brackets to limit the search ****
    |------------------------------------------------------|
    | Tag    | Meaning                                     |
    | ------ | --------------------------------------------|
    | [TI]   | Title                                       |
    | [AB]   | Abstract                                    |
    | [TIAB] | Title or Abstract                           |
    | [AU]   | Author                                      |
    | [AD]   | Author Affiliation                          |
    | [MH]   | MeSH Terms                                  |
    | [TW]   | Text Word (all searchable fields)           |
    | [PT]   | Publication Type                            |
    | [LA]   | Language                                    |
    | [DP]   | Date of Publication                         |
    | [TA]   | Journal Title (abbreviated)                 |
    | [SID]  | Secondary Source ID (e.g., clinical trials) |
    |------------------------------------------------------|

    EXAMPLE : "cancer therapy"[TIAB] AND "Pfizer"[AD]

    **** Use double quotes to search for exact phrases ****
    EXAMPLE : "gene therapy" OR "cell therapy"

    **** Wildcards and Truncation ****
    (*)  wildcard for 0 or more characters
    EXAMPLE : pharma* -> pharma, pharmaceutical, pharmaceuticals

    No ? or single-character wildcard.

    **** Date Filtering ****
    Use [DP] (Date of Publication):
    EXAMPLE : ("2020"[DP] : "2025"[DP]) AND diabetes
    EXAMPLE : "last 5 years"[PDat]

    **** MeSH (Medical Subject Headings) ****
    [MH] = MeSH Term
    EXAMPLE : "Diabetes Mellitus"[MH]

    To explode the MeSH term (include subcategories), just use [MH].
    To not explode, use [MH:NOEXP].

    **** Other Useful Filters ****
    |-------------------------------------------------|
    | Filter       | example                          |
    | ------------ | ---------------------------------|
    | Language     | english[LA]                      |
    | Species      | humans[MeSH Terms]               |
    | Age Group    | adult[MeSH Terms]                |
    | Article Type | review[PT], clinical trial[PT]   |
    |-------------------------------------------------|

    **** Author and Institution Search ****
    EXAMPLES : Smith JA[AU] AND Pfizer[AD]
                "Roche Diagnostics"[AD]
                "University of Oxford"[AD]

    --EXAMPLE with many feature combined--
    ("machine learning"[TIAB] OR "deep learning"[TIAB]) 
    AND (cancer[TIAB] OR oncology[TIAB]) 
    AND (pharma*[AD] OR biotech*[AD] OR "Pfizer"[AD]) 
    AND ("2019"[DP] : "2024"[DP])

    -- end of page --

"
elif [[ "$input" == "-f" || "$input" == "--file" ]]; then
    echo "will add later!"
    date

elif [[ "$input" == "exit" ]]; then
    echo "bye!"
        break
        
else
    echo "Unrecognized command."

fi
done