import threading
from agent import start_watcher
from email_fetcher import start_email_fetcher

threading.Thread(target=start_watcher).start()
threading.Thread(target=start_email_fetcher).start()