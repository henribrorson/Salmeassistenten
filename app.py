import streamlit as st
import json
import os
import openai

# API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load salmedatabase
with open("salmer.json", "r", encoding="utf-8") as f:
    database = json.load(f)

salmer = database["salmer"]


def find_temaer(input_text):
    """
    Får OpenAI til at identificere centrale temaer
    """

    prompt = f"""
Du er teologisk assistent.

Analyser følgende bibeltekster og returnér KUN en kommasepareret liste over centrale temaer.

Tekster:

{input_text}

Eksempel:
guds omsorg, tillid, håb, frelse, nåde
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Du identificerer teologiske hovedtemaer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        temaer = response.choices[0].message.content

        return [
            t.strip().lower()
            for t in temaer.split(",")
            if t.strip()
        ]

    except Exception:
        return []


def score_salme(salme, temaer):

    score = 0

    for tema in temaer:

        if tema in [t.lower() for t in salme["temaer"]]:
            score += 5

        if tema in [t.lower() for t in salme["bibelske_motiver"]]:
            score += 3

        if tema in [t.lower() for t in salme["noegleord"]]:
            score += 1

    return score


def find_relevante_salmer(input_text):

    temaer = find_temaer(input_text)

    resultater = []

    for salme in salmer:

        score = score_salme(salme, temaer)

        resultater.append(
            {
                "salme": salme,
                "score": score
            }
        )

    resultater.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return temaer, resultater[:10]


st.title("Salmeassistent")

gt = st.text_area("GT")
epistel = st.text_area("Epistel")
evangelium = st.text_area("Evangelium")

if st.button("Find salmer"):

    input_text = f"""
GT:
{gt}

Epistel:
{epistel}

Evangelium:
{evangelium}
"""

    with st.spinner("Analyserer tekster ..."):

        temaer, resultater = find_relevante_salmer(input_text)

    st.subheader("Identificerede temaer")

    st.write(", ".join(temaer))

    st.subheader("Foreslåede salmer")

    for r in resultater:

        salme = r["salme"]

        st.write(
            f"**DDS {salme['nr']} – {salme['titel']}** "
            f"(score: {r['score']})"
        )

        st.caption(
            "Temaer: "
            + ", ".join(salme["temaer"])
        )
