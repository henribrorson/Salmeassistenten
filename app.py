import streamlit as st
import json
import numpy as np
import os
import openai

# Set API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load data
with open("salmer_embeddings.json", "r", encoding="utf-8") as f:
    data = json.load(f)["salmer"]

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_relevant_salmer(input_text):
    # Midlertidig fallback (uden embeddings)
    return data[:20]

st.title("Salmeassistent")

gt = st.text_area("GT")
epistel = st.text_area("Epistel")
evangelium = st.text_area("Evangelium")

if st.button("Find salmer"):

    st.subheader("Forslag til salmer")

    salmer = find_relevant_salmer(gt + epistel + evangelium)

    for s in salmer:
        st.write(f"{s['nr']} – {s['titel']}")
