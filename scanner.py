import os, uuid, shutil
from datetime import datetime
from plyer import notification
import joblib

# Load model
model = joblib.load("sample_model.pkl")

def quarantine_text(content):
    if not os.path.exists("sandbox"):
        os.makedirs("sandbox")
    unique_name = f"{uuid.uuid4().hex}.txt"
    dest_path = os.path.join("sandbox", unique_name)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"🚨 Quarantined: {dest_path}")
    return dest_path

def log_quarantine(source, prediction):
    with open("sandbox/log.txt", "a") as log:
        log.write(f"{datetime.now()} | {source} | {prediction}\n")

def scan_message(content, source="unknown"):
    label_map = {0: "safe", 1: "scam"}
    prediction_raw = model.predict([content])[0]
    prediction = label_map[prediction_raw]
    print(f"🔮 Prediction from {source}: {prediction}")

    if prediction == "scam":
        notification.notify(
            title="⚠️ Scam Alert",
            message=f"Suspicious message detected from {source}",
            timeout=5
        )
        quarantine_text(content)
        log_quarantine(source, prediction)

    return prediction