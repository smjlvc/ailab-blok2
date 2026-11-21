# GirlTHing AI Lab — Blok 2: Studentski asistent

| Datoteka | Šta je |
|---|---|
| `data/` | dokumenti baze znanja (.pdf, .md, .txt) |
| `rag.py` | RAG logika: učitavanje, chunking, embeddings, pretraga, odgovor (R6) |
| `app.py` | web aplikacija u Streamlitu (R7) |
| `eval.py` | mjerenje kvaliteta na test setu (R7) |
| `test_set.json` | 10 pitanja s očekivanim odgovorima i izvorima |

## Pokretanje aplikacije

**GitHub Codespaces (ništa se ne instalira):** na GitHubu kliknite *Code → Codespaces → Create codespace on master*. Paketi se instaliraju sami. U datoteku `.env` upišite ključ, pa u terminalu:

```bash
streamlit run app.py
```

**Lokalno (VS Code):**

```bash
pip install -r requirements.txt
cp .env.example .env        # Windows: copy .env.example .env
# upišite ključ u .env
streamlit run app.py        # ako ne radi: python -m streamlit run app.py
```

Aplikacija se otvara na http://localhost:8501.

## Evaluacija

```bash
python eval.py
```

Cilj: bar 8/10. Pokrenite nakon svake izmjene prompta ili dokumenata.

Nove dokumente samo dodajte u `data/` — indeks (`index.npz`) se sam ponovo napravi.
