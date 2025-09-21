import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import csv
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# 1. Load and clean the dataset

data = pd.read_csv(
    'sample.csv',
    header=None,
    names=['messages', 'label'],
    encoding='utf-8',
    quoting=csv.QUOTE_NONE,
    quotechar='"',
    on_bad_lines='skip',
    engine='python'
)
data['label'] = data['label'].astype(int)
data['messages'] = data['messages'].astype(str).str.lower()
data = data.dropna(subset=['messages'])
data = data[data['messages'].str.strip() != '']
print("📄 Columns in dataset:", data.columns.tolist())
print("✅ Dataset loaded successfully.")
print(data.head())

# 🔹 2. Clean the raw text
def clean_text(text):
    # Keep URLs and digits, just normalize whitespace and lowercase
    text = re.sub(r"[^\w\s:/.]", "", text)  # remove weird punctuation but keep : / . for links
    text = re.sub(r"\s+", " ", text)        # normalize whitespace
    return text.lower().strip()

# 🔹 3. Drop empty or null messages
data = data.dropna(subset=['messages'])
data = data[data['messages'].str.strip() != '']

# 🔹 4. Optional: Add custom features (can be used later)
data['has_link'] = data['messages'].str.contains(r"http\S+").astype(int)
data['has_money'] = data['messages'].str.contains(r"\brs\b|\bdollar\b|\bwin\b").astype(int)


# 2. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    data['messages'], data['label'], test_size=0.2, random_state=42
)

print("🧹 Checking for empty messages...")
print(X_train.isnull().sum())
print(X_train.str.strip().eq('').sum())

# 3. Build the model pipeline
model = make_pipeline(
    TfidfVectorizer(stop_words='english', ngram_range=(1, 2)),
    MultinomialNB()
)
print("✅ Model pipeline created.")

# 4. Train the model
print("🔍 Sample messages:", X_train[:5].tolist())
print("📏 Total messages:", len(X_train))
model.fit(X_train, y_train)

# 5. Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# 6. Save the model
joblib.dump(model, "sample_model.pkl")
print("✅ Model trained and saved as sample_model.pkl")