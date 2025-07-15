import threading, yaml, time
from src.email_api import get_email_api_query
from src.esearcher import make_esearch_call
from src.efetcher_and_parser import make_efetch_call_and_parse
from src.utils import make_csv
from src.queues import fetch_queue, data_queue, shutdown_event


with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)


def main(webenv:str, query_key:str, email:str, api_key:str) -> None:
    start_time = time.time()
    print("Starting threads.")

    rate_limit = config["ncbi"]["rate_limit"]  # per second
    retmax = config["ncbi"]["retmax"]
    total_fetchable_records = config["ncbi"]["total_fetchable_records"]  
    num_fetch_threads = config["ncbi"]["num_fetch_threads"]
    
    if api_key:
        num_fetch_threads = config["ncbi"]["num_fetch_threads_with_api"]

    output_file = f"outputs/{email}.csv"

    #Fill the fetch queue with start(retstart) for each fetch call
    for start in range(0, total_fetchable_records, retmax):
        fetch_queue.put(start)
    
    writer = threading.Thread(target=make_csv, args=(output_file,))
    writer.start()
    

    # Start fetch threads
    fetch_threads = []
    for i in range(num_fetch_threads):
        t = threading.Thread(target=make_efetch_call_and_parse, args=(i+1, webenv, query_key, email, api_key))
        t.start()
        fetch_threads.append(t)

    # Wait for fetch to complete
    fetch_queue.join()

    # Wait for data queue to empty
    data_queue.join()

    # Signal writer to shut down
    shutdown_event.set()
    writer.join()
    end_time = time.time()
    print("All threads done.")
    print(f"Time taken {end_time - start_time:.4f} sec")

if __name__ == "__main__":

    email, api_key, query = get_email_api_query()
    count, webenv, query_key = make_esearch_call(query = query, email=email, api_key=api_key)
    main(webenv =webenv, query_key = query_key, email = email, api_key = api_key)