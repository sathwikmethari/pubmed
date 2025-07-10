# PubMed Fetcher
## Files
<h4>Main folder has 2 sub folders, 8 files</h4>
  <ul>
    <li>main.py is the starting point, when run opens shell.</li>
    <li>Inside the shell if chosen correct command runs main_2.py(most of src files are called here) file.</li>
    <li>config.yaml has configuration settings.</li>
    <li>poetry.lock, pyproject.toml are made during poetry build.</li>
    <li>.gitignore, README.md, requirements.txt files.</li>    
  </ul>
<h4>src</h4>
  <ul>
    <li>email_api.py file has a function that gets email, api, query from the user.</li>
    <li>esearcher.py file checks for valid query, if valid gets webenv, query_key. Required for getting results.</li>
    <li>efetcher_and_parser.py has function to fetch xml results(with webenv, query_key) and parses them.</li>
    <li>script.sh for shell commands.</li>
    <li>utils.py for important functions, classes.</li>
    <li>queues.py for queue objects for multiple threads.</li>
    <li>file_list.py for functionality.</li>  
  </ul>
<h4>outputs</h4>
  <ul>
    <li>Folder containg the data obtained from fetches in a csv.</li>
  </ul>

## Imp
1. Had to cut max records fetch to 10K. Tried various methods to get above this limit, couldn't find any.
2. Can tinker around with filters, thread numbers in config (default=3).
3. There is Server Latency from NCBI (expected). 

## Instructions
<ul>
    <li>Install poetry <code>pipx install poetry</code></li>
    <li>Clone the repository <code>https://github.com/sathwikmethari/pubmed.git</code></li>
    <li>While in the folder <code>poetry install</code></li>
    <li>run the main file <code>poetry run python main.py</code></li>
    <li><code>poetry run get-papers-list</code> prints downloaded csv files.</li>  
  </ul>
  
### Tools
1. requests, pandas, pyyaml libraries.
2. Used LLM to generate filters for NCGI, shell script(syntax only), resolving poetry errors, some sections of this readme.
3. [NCBI](https://www.ncbi.nlm.nih.gov/books/NBK25499/) for information about esearch, efetch.
