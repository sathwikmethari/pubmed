# queues to be imported in files
import queue
import threading

fetch_queue = queue.Queue()
data_queue = queue.Queue()
shutdown_event = threading.Event()
