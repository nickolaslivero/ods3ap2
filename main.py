import pandas as pd
import json
import os
import re

# Função para limpar textos (letras)
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove espaços em excesso
    text = re.sub(r'[^\w\s]', '', text)  # Remove pontuações
    return text.strip()

dataset_path = "./LLM Bois"

data = []

for boi in os.listdir(dataset_path):
    boi_path = os.path.join(dataset_path, boi)
    
    if os.path.isdir(boi_path):
        for filename in os.listdir(boi_path):
            filepath = os.path.join(boi_path, filename)
            
            if filename.endswith(".txt"):
                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.read().strip()
                    lines = content.split("\n")
                    
                    boi_nome = lines[1].replace("Boi: ", "").strip()
                    letra = clean_text(" ".join(lines[2:])) 
                    
                    data.append({"boi": boi_nome, "letra": letra})

def format_to_jsonl(dataset, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for _, row in dataset.iterrows():
            json.dump({
                "instruction": "Você é um assistente que responde perguntas sobre os bois bumbás e cria músicas do Boi Garantido e Caprichoso levando em conta suas características",
                "input": f"Crie uma música do boi {row['boi']} levando em conta suas características",
                "output": row["letra"]
            }, f, ensure_ascii=False)
            f.write('\n')


df = pd.DataFrame(data)

df = df[df["letra"].notnull() & df["letra"].str.strip().ne("")]

filename = "dataset_musicas.jsonl"

format_to_jsonl(df, filename)
