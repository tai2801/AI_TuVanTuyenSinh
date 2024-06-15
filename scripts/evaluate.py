"""Danh gia mo hinh tren test_set.json doc lap: accuracy, fallback, confusion tom tat.

Chay: python scripts/evaluate.py  (tu goc du an, sau khi da cai requirements)
"""
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.chatbot import Chatbot
from app.knowledge import DATA_DIR, KnowledgeBase
from app.train import load_model


def main():
    kb = KnowledgeBase()
    bot = Chatbot(kb, load_model())
    with open(os.path.join(DATA_DIR, "test_set.json"), encoding="utf-8") as f:
        cases = json.load(f)["cases"]
    correct = 0
    fb_ok = 0
    confusions = Counter()
    per_intent = Counter()
    per_intent_ok = Counter()
    for i, c in enumerate(cases):
        res = bot.reply(f"eval-{i}", c["text"])
        pred_ok = res["intent"] == c["intent"]
        # Cau ngoai pham vi: dung khi fallback duoc kich hoat (intent co the la ngoai_pham_vi)
        if c["expect_fallback"]:
            pred_ok = res["fallback"] is True
            fb_ok += 1 if res["fallback"] else 0
        per_intent[c["intent"]] += 1
        if pred_ok:
            correct += 1
            per_intent_ok[c["intent"]] += 1
        else:
            confusions[(c["intent"], res["intent"])] += 1
    n = len(cases)
    n_fb = sum(1 for c in cases if c["expect_fallback"])
    print(f"Test set: {n} cau")
    print(f"Accuracy (intent dung; ngoai pham vi tinh dung khi fallback): {correct}/{n} = {correct/n:.3f}")
    if n_fb:
        print(f"Fallback dung tren cau ngoai pham vi: {fb_ok}/{n_fb}")
    print("\nTheo intent:")
    for intent in sorted(per_intent):
        print(f"  {intent:24s} {per_intent_ok[intent]}/{per_intent[intent]}")
    print("\nNhom nham lan (expected -> predicted):")
    for (e, p), c in confusions.most_common():
        print(f"  {e} -> {p}: {c}")
    if not confusions:
        print("  (khong co)")


if __name__ == "__main__":
    main()
