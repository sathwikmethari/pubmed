import queue, threading
import pandas as pd

shutdown_event=threading.Event()
data_queue=queue.Queue()

def make_csv(output_file):
    buffer = []
    while not shutdown_event.is_set() or not data_queue.empty():
        try:
            data = data_queue.get(timeout=1)
            buffer.append(data.to_dict())
            data_queue.task_done()
        except queue.Empty:
            continue

    # Final save
    df = pd.DataFrame(buffer)
    df.to_csv(output_file, index=False)
    print(f"[Writer] Saved {len(buffer)} records to {output_file}")