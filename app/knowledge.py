"""Nap va quan ly du lieu tuyen sinh (JSON trong data/) + CRUD cho admin."""
import json
import os
import threading

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
_lock = threading.Lock()


def _load(name):
    with open(os.path.join(DATA_DIR, name), encoding="utf-8") as f:
        return json.load(f)


def _save(name, payload):
    with _lock:
        with open(os.path.join(DATA_DIR, name), "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=1)


class KnowledgeBase:
    def __init__(self):
        self.reload()

    def reload(self):
        self.majors_doc = _load("majors.json")
        self.methods_doc = _load("admission_methods.json")
        self.faqs_doc = _load("faqs.json")
        self.majors = self.majors_doc["majors"]
        self.methods = self.methods_doc["methods"]
        self.faqs = self.faqs_doc["faqs"]

    # --- majors CRUD ---
    def get_major(self, code):
        for m in self.majors:
            if m["code"].upper() == str(code).upper():
                return m
        return None

    def upsert_major(self, major):
        existing = self.get_major(major["code"])
        if existing:
            existing.update(major)
        else:
            self.majors.append(major)
        _save("majors.json", self.majors_doc)
        return major

    def delete_major(self, code):
        before = len(self.majors)
        self.majors_doc["majors"] = [m for m in self.majors if m["code"].upper() != str(code).upper()]
        self.majors = self.majors_doc["majors"]
        _save("majors.json", self.majors_doc)
        return len(self.majors) < before

    # --- faq CRUD ---
    def upsert_faq(self, faq):
        for f in self.faqs:
            if f["id"] == faq["id"]:
                f.update(faq)
                _save("faqs.json", self.faqs_doc)
                return faq
        self.faqs.append(faq)
        _save("faqs.json", self.faqs_doc)
        return faq

    def delete_faq(self, faq_id):
        before = len(self.faqs)
        self.faqs_doc["faqs"] = [f for f in self.faqs if f["id"] != faq_id]
        self.faqs = self.faqs_doc["faqs"]
        _save("faqs.json", self.faqs_doc)
        return len(self.faqs) < before

    def faq_by_topic(self, topic):
        return [f for f in self.faqs if f.get("topic") == topic]
