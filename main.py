import queue, threading, os
from files.src.esearcher import make_esearch_call
from files.src.efetcher_and_parser import make_efetch_call__and_parse
from files.src.save_to_csv import make_csv

RETMAX = 100
TOTAL_RECORDS = 1000
RATE_LIMIT = 10
NUM_FETCH_THREADS = 3

fetch_queue = queue.Queue()
data_queue = queue.Queue()
shutdown_event = threading.Event()

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
    for _ in range(NUM_FETCH_THREADS):
        t = threading.Thread(target=make_efetch_call__and_parse)
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
    pass