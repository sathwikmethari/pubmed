import os, threading
from dotenv import load_dotenv
from src.esearcher import make_esearch_call
from src.efetcher_and_parser import make_efetch_call__and_parse
from src.save_to_csv import make_csv
from src.queues import fetch_queue, data_queue, shutdown_event

load_dotenv()

RETMAX = 1000
RATE_LIMIT = 10
NUM_FETCH_THREADS = 3


query = "covid-19 AND 2024[dp] AND humans[MeSH Terms]"
NCBI_API_KEY = os.getenv("NCBI_API_KEY")
NCBI_EMAIL = os.getenv("email")
TOTAL_RECORDS, webenv, query_key = make_esearch_call(query = query, api_key = NCBI_API_KEY, email = NCBI_EMAIL)

def main():
    #Fill the fetch queue with start(retstart) for each fetch call
    for start in range(0, TOTAL_RECORDS, RETMAX):
        fetch_queue.put(start)

    # Start writer
    output_file = "output.csv"
    writer = threading.Thread(target=make_csv, args=(output_file,))
    writer.start()

    # Start fetch threads
    fetch_threads = []
    for i in range(NUM_FETCH_THREADS):
        t = threading.Thread(target=make_efetch_call__and_parse,args=(i+1, webenv, query_key, NCBI_EMAIL, NCBI_API_KEY))
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

if __name__ == "__main__":        
    main()