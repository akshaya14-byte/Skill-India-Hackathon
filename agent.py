import time
import os
import joblib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from plyer import notification
import pandas as pd

# Load trained model
model = joblib.load("sample_model.pkl")

class WatcherHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".txt"):
            print(f"📂 New file detected: {event.src_path}")

            # Retry reading until file is free
            for i in range(5):
                try:
                    with open(event.src_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    break  # ✅ Success, exit loop
                except PermissionError:
                    print("⏳ File is busy, retrying...")
                    time.sleep(1)
            else:
                print("❌ Could not read file after retries.")
                return

            # Predict with model
            label_map = {0: "safe", 1: "scam"}
            prediction_raw = model.predict([content])[0]
            prediction = label_map[prediction_raw]
            print(f"🔮 Prediction: {prediction}")
            

            if prediction == "scam":
                print("⚠️ Scam detected!")
                notification.notify(
                title="⚠️ Scam Alert",
                message="Suspicious message detected",
                timeout=5
)

                

def start_watcher(path="watch_folder"):
    if not os.path.exists(path):
        os.makedirs(path)

    event_handler = WatcherHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    print(f"👀 Watching folder: {path}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    start_watcher()
