import queue
import pandas as pd
from queues import data_queue, shutdown_event

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
    df["NonAcademicAuthors"] = df["NonAcademicAuthors"].apply(lambda x: ", ".join(x))
    df["CompanyAffiliations"] = df["CompanyAffiliations"].apply(lambda x: ", ".join(x))
    df.to_csv(output_file, index=False)
    print(f"[Writer] - Saved {len(buffer)} records to {output_file}")