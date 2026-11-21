"""
app.py — web aplikacija Studentskog asistenta (Streamlit).

Pokretanje:  streamlit run app.py
(ako komanda nije pronađena:  python -m streamlit run app.py)

Ključna ideja Streamlita: svaki klik ponovo pokreće CIJELU skriptu od vrha.
Zato koristimo st.session_state (pamti razgovor) i @st.cache_resource (indeks se pravi jednom).
"""

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

import rag

ROOT = Path(__file__).resolve().parent
MAX_QUESTION_CHARS = 500   # najduže dozvoljeno pitanje (zaštita od zloupotrebe)
MAX_QUESTIONS = 20         # najviše pitanja po razgovoru (kontrola troškova)

# ---------------------------------------------------------------- stranica
st.set_page_config(page_title="Studentski asistent", page_icon="🎓")
st.title("🎓 Studentski asistent")

with st.sidebar:
    st.header("O asistentu")
    st.write(
        "Odgovaram na pitanja o CV-u, razgovoru za posao, GitHub i LinkedIn profilu, "
        "učenju programiranja, stipendijama i programu GirlTHing AI Lab."
    )
    st.caption("Odgovori su samo iz naše baze znanja. Ispod svakog odgovora su izvori.")
    if st.button("🔄 Novi razgovor"):
        st.session_state.messages = []
        st.rerun()

# ---------------------------------------------------------------- klijent i indeks
load_dotenv(ROOT / ".env")
if not os.getenv("OPENAI_API_KEY"):
    st.error("Nedostaje OPENAI_API_KEY. Napravi datoteku .env pored app.py (kopija .env.example) i upiši ključ.")
    st.stop()


@st.cache_resource
def get_client():
    return OpenAI()


@st.cache_resource(show_spinner="Pripremam bazu znanja...")
def get_index():
    return rag.load_or_build_index(get_client(), ROOT / "data", ROOT / "index.npz")


client = get_client()
index = get_index()

# ---------------------------------------------------------------- historija razgovora
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m.get("sources"):
            st.caption("Izvori: " + ", ".join(m["sources"]))

# ---------------------------------------------------------------- novo pitanje
question = st.chat_input("Pitaj nešto...")

if question:
    broj_pitanja = sum(m["role"] == "user" for m in st.session_state.messages)
    if len(question) > MAX_QUESTION_CHARS:
        st.warning(f"Pitanje je predugo (najviše {MAX_QUESTION_CHARS} znakova).")
    elif broj_pitanja >= MAX_QUESTIONS:
        st.warning("Dostignut je limit pitanja u ovom razgovoru. Klikni „Novi razgovor“.")
    else:
        with st.chat_message("user"):
            st.markdown(question)

        history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        with st.chat_message("assistant"):
            try:
                stream, sources = rag.answer(client, index, question, history=history, stream=True)
                odgovor = st.write_stream(stream)
            except Exception as e:
                st.error(f"Greška pri komunikaciji s modelom: {e}")
                st.stop()
            if sources:
                st.caption("Izvori: " + ", ".join(sources))

        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.messages.append({"role": "assistant", "content": odgovor, "sources": sources})
