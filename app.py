import streamlit as st
import json
import numpy as np
import os
from openai import OpenAI

client = OpenAI()

with open("salmer_embeddings.json", "r", encoding="utf-8") as f:
    data = json.load(f)["salmer"]

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_relevant_salmer(input_text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=input_text
    )
    input_embedding = response.data[0].embedding

    scored = []
    for salme in data:
        if "embedding" in salme:
            sim = cosine_similarity(input_embedding, salme["embedding"])
            scored.append((sim, salme))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [s[1] for s in scored[:30]]

st.title("Salmeassistent")

gt = st.text_area("GT")
epistel = st.text_area("Epistel")
evangelium = st.text_area("Evangelium")

if st.button("Find salmer"):

    input_text = f"GT: {gt}\nEpistel: {epistel}\nEvangelium: {evangelium}"

    top_salmer = find_relevant_salmer(input_text)

    st.subheader("Top 30 relevante salmer")

    for s in top_salmer:
        st.write(f"{s['nr']} – {s['titel']}")
