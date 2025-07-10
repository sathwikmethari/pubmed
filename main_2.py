import threading, yaml
from src.esearcher import make_esearch_call
from src.efetcher_and_parser import make_efetch_call__and_parse
from src.email_api import get_email_api_query
from src.utils import make_csv
from src.queues import fetch_queue, data_queue, shutdown_event


with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# rate_limit = config["ncbi"]["rate_limit"]  # per second
# retmax = config["ncbi"]["retmax"]
# num_fetch_threads = config["ncbi"]["num_fetch_threads"]
# total_fetchable_records = config["ncbi"]["total_fetchable_records"]  


def main(webenv:str, query_key:str, email:str, api_key:str) -> None:
    #Fill the fetch queue with start(retstart) for each fetch call
    rate_limit = config["ncbi"]["rate_limit"]  # per second
    retmax = config["ncbi"]["retmax"]
    num_fetch_threads = config["ncbi"]["num_fetch_threads"]
    total_fetchable_records = config["ncbi"]["total_fetchable_records"]  


    output_file = f"outputs/{email}.csv" 
    for start in range(0, total_fetchable_records, retmax):
        fetch_queue.put(start)
    writer = threading.Thread(target=make_csv, args=(output_file,))
    writer.start()
    #print(num_fetch_threads)
    if api_key:
        num_fetch_threads = 5

    # Start fetch threads
    fetch_threads = []
    for i in range(num_fetch_threads):
        t = threading.Thread(target=make_efetch_call__and_parse,args=(i+1, webenv, query_key, email, api_key))
        t.start()
        fetch_threads.append(t)

    # Wait for fetch to complete
    fetch_queue.join()

    # Wait for data queue to empty
    data_queue.join()

    # Signal writer to shut down
    shutdown_event.set()
    writer.join()

    print("All threads done.")
    print("Total time taken != sum of all times")

if __name__ == "__main__":
    email, api_key, query = get_email_api_query(base_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi")
    #query = "covid-19 AND 2024[dp] AND humans[MeSH Terms]"
    query_is_valid, count, webenv, query_key = make_esearch_call(query = query, email=email, api_key=api_key)
    if query_is_valid:
        make_efetch_call__and_parse(worker_id = 1, webenv = webenv, query_key = query_key, email = email, api_key = api_key)
        main(webenv =webenv, query_key = query_key, email = email, api_key = api_key)
    else:
        print("Enter a valid query!")