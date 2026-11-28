# DEPLOY.md: od laptopa do javnog linka

Ovo uputstvo vodi te od aplikacije koja radi na tvom računaru do javnog linka oblika `ime.streamlit.app`, koji možeš poslati bilo kome.

```
Laptop  →  GitHub (kod BEZ ključa)  →  Streamlit Community Cloud (ključ u Secrets)  →  javni link
```

> ⚠️ **API ključ nikad ne ide na GitHub.** Prije svakog commita pokreni `git status` i provjeri da se `.env` NE nalazi na listi. Ako ključ ikad završi na GitHubu, odmah ga poništi u OpenAI dashboardu (API keys → Revoke) i napravi novi. To vrijedi i ako ga obrišeš iz koda, jer ostaje u historiji.

---

## Prije početka

- [ ] Aplikacija radi lokalno: `streamlit run app.py`
- [ ] `python eval.py` daje bar 8/10
- [ ] Imaš GitHub račun
- [ ] U OpenAI dashboardu je postavljen **limit potrošnje projekta** (Settings → Limits)

---

## Dio 1: Kod na GitHub

Treba ti **tvoj** repozitorij sa sljedećim fajlovima: `app.py`, `rag.py`, `requirements.txt`, folder `data/` i ostali fajlovi iz repozitorija. **Bez `.env`.**

### Opcija A: fork (najlakše)

1. Otvori repozitorij programa na GitHubu i gore desno klikni **Fork → Create fork**. Sad imaš svoju kopiju: `github.com/TVOJE-IME/girlthing-ai-lab-blok2`.
2. Ako si mijenjala `app.py` (naslov, dugmad iz R7), u svom forku otvori `app.py`, klikni ikonu olovke ✏️, zalijepi svoju verziju i klikni **Commit changes**.
3. Svoje dokumente dodaješ ovako: otvori folder `data`, pa **Add file → Upload files**.

### Opcija B: preko terminala (git)

U folderu projekta, u terminalu u VS Code-u:

```bash
git status                       # .env NE smije biti na listi!
git add .
git commit -m "Moj Studentski asistent"
git push
```

Ako je projekat preuzet s tuđeg repozitorija, prvo napravi fork (opcija A, korak 1), pa ga poveži:

```bash
git remote set-url origin https://github.com/TVOJE-IME/girlthing-ai-lab-blok2.git
git push -u origin HEAD
```

### Opcija C: upload preko web sučelja

Ako se ne snalaziš s terminalom: na GitHubu napravi novi repozitorij (**New → Public**), pa **Add file → Upload files** i prevuci sve fajlove i folder `data`. **Ne uploaduj `.env`.**

---

## Dio 2: Objava na Streamlit Community Cloud

1. Otvori **share.streamlit.io** i prijavi se GitHub računom (**Continue with GitHub**).
2. Klikni **Create app**, pa **„Yup, I have an app“**.
3. Popuni:
   - **Repository:** `TVOJE-IME/girlthing-ai-lab-blok2`
   - **Branch:** grana u kojoj je kod, obično `main`, ali može biti i `master` (provjeri na GitHubu, iznad liste fajlova)
   - **Main file path:** `app.py`
4. **App URL:** izaberi ime, npr. `studentski-asistent-amra`. Ime mora biti jedinstveno.
5. Klikni **Advanced settings** i u polje **Secrets** upiši (format je isti kao u `.streamlit/secrets.toml.example`):

   ```toml
   OPENAI_API_KEY = "sk-...tvoj ključ..."
   ```

   Klikni **Save**.
6. Klikni **Deploy**. Prva objava traje 2–5 minuta, jer server instalira pakete i pravi indeks. Kad se aplikacija otvori, postavi jedno pitanje i pošalji link u grupni chat. 🎉

Kasnije izmjene: svaki novi commit na GitHubu Streamlit Cloud automatski objavi za minutu-dvije.

---

## Kad nešto ne radi

| Poruka | Uzrok | Rješenje |
|---|---|---|
| `ModuleNotFoundError` | Paket nije u `requirements.txt` | Dodaj paket u `requirements.txt`, commit, push |
| „Nedostaje OPENAI_API_KEY“ | Secret nije upisan ili ima drugi naziv | App settings (⋮ → Settings) → Secrets; naziv mora biti tačno `OPENAI_API_KEY` |
| Greška 401 | Pogrešan ili poništen ključ | Napravi novi ključ i zamijeni ga u Secrets |
| Greška 429 | Dostignut limit potrošnje | Provjeri limit projekta u OpenAI dashboardu |
| Aplikacija „spava“ | Dugo nije korištena | Klikni „Yes, get this app back up“ i sačekaj minutu |
| Ne vidi se repozitorij | Streamlit nema pristup GitHubu | Na share.streamlit.io: Settings → Linked accounts → GitHub → odobri pristup |
| „Branch does not exist“ | Pogrešna grana | Provjeri na GitHubu da li je `main` ili `master` |
| Odgovori ne znaju nove dokumente | Dokumenti nisu na GitHubu | Upload u `data/`, commit; aplikacija sama ponovo napravi indeks |

Za detaljniji pregled greške: dolje desno u aplikaciji klikni **Manage app**, pa pogledaj log.

---

## Šablon prezentacije: demo od 5 minuta

| Vrijeme | Dio | Šta kažeš i pokazuješ |
|---|---|---|
| 0:00–0:45 | **Problem** | Ko ima problem i zašto je važan, kroz jednu konkretnu situaciju („Amra je studentica prve godine i…“) |
| 0:45–1:30 | **Rješenje** | Šta je tvoj chatbot, za koga je i iz kojih dokumenata odgovara |
| 1:30–3:30 | **Demo uživo** | 2–3 pripremljena pitanja i **jedno na koje chatbot pošteno kaže „ne znam“**. Pokaži izvore ispod odgovora. |
| 3:30–4:15 | **Kako radi** | Jedan slajd: pitanje → pretraga → model → odgovor s izvorima, uz rezultat evaluacije (npr. **9/10**) |
| 4:15–5:00 | **Šta dalje** | Šta bi dodala, šta si naučila, link na aplikaciju |

**Savjeti:**

- Počni od osobe i problema, a ne od tehnologije.
- Pokaži „ne znam“: chatbot koji ne izmišlja ulijeva povjerenje.
- Koristi broj umjesto pridjeva: „9/10 tačnih“, a ne „radi odlično“.
- Snimi video demoa kao rezervu, ako internet ili API zakažu (Windows: Win + Alt + R; Mac: Cmd + Shift + 5).

**Mini nastup na radionici (2 minute):** 20 s jedna rečenica o problemu → 80 s demo s 2 pitanja na javnom linku → 20 s jedna stvar koju si naučila.

---

## Checklista prije nastupa

- [ ] Aplikacija je objavljena i link radi u privatnom prozoru preglednika
- [ ] Ključ je samo u Secrets, ne na GitHubu (`.env` nije u repozitoriju)
- [ ] Postavljen je limit potrošnje projekta; `MAX_QUESTIONS` je u `app.py`
- [ ] `python eval.py` daje bar 8/10, a rezultat je na slajdu
- [ ] Pripremljena su 2–3 pitanja + jedno „ne znam“ pitanje
- [ ] Prije nastupa je otvorena aplikacija (da ne „spava“) i postavljeno je jedno probno pitanje
- [ ] Snimljen je video kao rezerva
- [ ] Prezentacija je izvježbana uz štopericu: do 5 minuta
