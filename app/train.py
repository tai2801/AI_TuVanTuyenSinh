"""Huan luyen mo hinh phan loai intent: TF-IDF (word + char n-gram) + Logistic Regression.

Ly do chon Logistic Regression thay LinearSVC: LR cho xac suat (predict_proba)
de tinh confidence va ap nguong fallback; LinearSVC khong co proba truc tiep.
Char n-gram 3-5 giup chiu duoc sai chinh ta nhe va viet tat.
"""
import json
import os
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion, Pipeline

from .knowledge import DATA_DIR
from .preprocess import normalize

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "models", "intent_model.pkl")


def load_training():
    with open(os.path.join(DATA_DIR, "training_data.json"), encoding="utf-8") as f:
        doc = json.load(f)
    X, y = [], []
    for intent, spec in doc["intents"].items():
        for p in spec["patterns"]:
            X.append(p)
            y.append(intent)
    return X, y


def build_pipeline():
    word = TfidfVectorizer(preprocessor=normalize, ngram_range=(1, 2), min_df=1)
    char = TfidfVectorizer(preprocessor=normalize, analyzer="char_wb",
                           ngram_range=(3, 5), min_df=1)
    feats = FeatureUnion([("word", word), ("char", char)])
    clf = LogisticRegression(max_iter=1000, C=8.0)
    return Pipeline([("features", feats), ("clf", clf)])


def train_and_save(path=MODEL_PATH):
    X, y = load_training()
    pipe = build_pipeline()
    pipe.fit(X, y)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(pipe, f)
    return pipe, len(X), len(set(y))


def load_model(path=MODEL_PATH):
    if not os.path.exists(path):
        pipe, _, _ = train_and_save(path)
        return pipe
    with open(path, "rb") as f:
        return pickle.load(f)


if __name__ == "__main__":
    pipe, n, k = train_and_save()
    print(f"Da huan luyen: {n} mau, {k} intent -> {MODEL_PATH}")
