{\rtf1\ansi\ansicpg1252\cocoartf2870
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\froman\fcharset0 Times-Roman;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs24 \cf0 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 import streamlit as st\
import json\
import numpy as np\
import os\
from openai import OpenAI\
\
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))\
\
# Load data\
with open("salmer_embeddings.json", "r", encoding="utf-8") as f:\
\'a0\'a0\'a0 data = json.load(f)["salmer"]\
\
# Cosine similarity\
def cosine_similarity(a, b):\
\'a0\'a0\'a0 return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))\
\
# Semantic search\
def find_relevant_salmer(input_text):\
\'a0\'a0\'a0 response = client.embeddings.create(\
\'a0\'a0\'a0\'a0\'a0\'a0\'a0 model="text-embedding-3-small",\
\'a0\'a0\'a0\'a0\'a0\'a0\'a0 input=input_text\
\'a0\'a0\'a0 )\
\'a0\'a0\'a0 input_embedding = response.data[0].embedding\
\
\'a0\'a0\'a0 scored = []\
\'a0\'a0\'a0 for salme in data:\
\'a0\'a0\'a0\'a0\'a0\'a0\'a0 sim = cosine_similarity(input_embedding, salme["embedding"])\
\'a0\'a0\'a0\'a0\'a0\'a0\'a0 scored.append((sim, salme))\
\
\'a0\'a0\'a0 scored.sort(reverse=True, key=lambda x: x[0])\
\'a0\'a0\'a0 return [s[1] for s in scored[:30]]\
\
# UI\
st.title("Salmeassistent")\
\
gt = st.text_area("GT")\
epistel = st.text_area("Epistel")\
evangelium = st.text_area("Evangelium")\
\
if st.button("Find salmer"):\
\
\'a0\'a0\'a0 input_text = f"""\
\'a0\'a0\'a0 GT: \{gt\}\
\'a0\'a0\'a0 Epistel: \{epistel\}\
\'a0\'a0\'a0 Evangelium: \{evangelium\}\
\'a0\'a0\'a0 """\
\
\'a0\'a0\'a0 top_salmer = find_relevant_salmer(input_text)\
\
\'a0\'a0\'a0 st.subheader("Top 30 relevante salmer")\
\
\'a0\'a0\'a0 for s in top_salmer:\
\'a0\'a0\'a0\'a0\'a0\'a0\'a0 st.write(f"\{s['nr']\} \'96 \{s['titel']\}")\
\
\'a0\'a0\'a0 prompt = f"""\
Du er pr\'e6st og salmeekspert.\
\
Tekster:\
GT: \{gt\}\
Epistel: \{epistel\}\
Evangelium: \{evangelium\}\
\
Her er 30 relevante salmer:\
\{top_salmer\}\
\
Udv\'e6lg:\
- 6\'968 st\'e6rkeste salmer\
- giv korte begrundelser\
- foresl\'e5 liturgisk brug\
\
Svar p\'e5 dansk.\
"""\
\
\'a0\'a0\'a0 response = client.chat.completions.create(\
\'a0\'a0\'a0\'a0\'a0\'a0\'a0 model="gpt-4.1",\
\'a0\'a0\'a0\'a0\'a0\'a0\'a0 messages=[\{"role": "user", "content": prompt\}]\
\'a0\'a0\'a0 )\
\
\'a0\'a0\'a0 st.subheader("AI-anbefaling")\
\'a0\'a0\'a0 st.write(response.choices[0].message.content)\
``\
}