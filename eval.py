"""
eval.py — mjeri kvalitet chatbota na test setu (test_set.json).

Pokretanje:  python eval.py
Pokrenite ga nakon svake izmjene prompta ili dokumenata. Traje 1–2 minute (oko 20 poziva API-ja).

Mjeri dvije stvari:
  1. Retrieval: da li je pretraga pronašla očekivani dokument (među TOP_K chunkova)?
  2. Odgovor:   da li je odgovor tačan? Ocjenjuje ga drugi poziv modela (LLM-as-a-judge).
"""

import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

import rag

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
client = OpenAI()


class Ocjena(BaseModel):
    tacno: bool
    obrazlozenje: str


JUDGE = """Ti si strog ocjenjivač odgovora chatbota.
Ako je očekivani odgovor "NEMA_ODGOVORA", odgovor je tačan samo ako chatbot kaže da nema tu informaciju.
Inače je tačan ako sadrži suštinu očekivanog odgovora (ne mora doslovno)."""


def judge(pitanje, ocekivano, odgovor):
    r = client.responses.parse(
        model=rag.CHAT_MODEL, instructions=JUDGE, text_format=Ocjena,
        input=f"PITANJE: {pitanje}\nOČEKIVANO: {ocekivano}\nODGOVOR: {odgovor}",
    )
    return r.output_parsed


def main():
    index = rag.load_or_build_index(client, ROOT / "data", ROOT / "index.npz")
    tests = json.load(open(ROOT / "test_set.json", encoding="utf-8"))

    # 1. Retrieval
    print("\n=== 1. Retrieval ===")
    pogoci, ukupno = 0, 0
    for t in tests:
        if not t["izvor"]:
            continue
        found = [c.source for c, _ in index.search(client, t["pitanje"], k=rag.TOP_K)]
        ukupno += 1
        if t["izvor"] in found:
            pogoci += 1
        else:
            print(f"❌ {t['pitanje']}\n    očekivano: {t['izvor']}  pronađeno: {found}")
    print(f"Retrieval hit rate: {pogoci}/{ukupno}")

    # 2. Odgovori
    print("\n=== 2. Odgovori (LLM-as-a-judge) ===")
    tacnih = 0
    for t in tests:
        odgovor, _ = rag.answer(client, index, t["pitanje"])
        o = judge(t["pitanje"], t["ocekivano"], odgovor)
        tacnih += o.tacno
        print("✅" if o.tacno else "❌", t["pitanje"])
        if not o.tacno:
            print("    odgovor:", odgovor[:200].replace("\n", " "))
            print("    sudija: ", o.obrazlozenje)

    print(f"\nREZULTAT: {tacnih}/{len(tests)} tačnih odgovora")
    print("Cilj za domaći: bar 8/10." if tacnih < 8 else "Cilj (8/10) postignut! 🎉")


if __name__ == "__main__":
    main()
