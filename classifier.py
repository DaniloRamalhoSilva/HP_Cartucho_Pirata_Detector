import os
import sqlite3
import time
from dotenv import load_dotenv
from openai import OpenAI

# 1) Configure sua API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 2) Prompt template (few-shot) para clareza
SYSTEM_PROMPT = (
    "Você é um assistente que recebe dados de um anúncio de cartucho HP "
    "e deve classificá-lo em **original** ou **suspeito** (pirata). "
    "Retorne apenas a palavra original ou suspeito."
)

FEW_SHOT_EXAMPLES = [
    {
        "title": "Cartucho HP 65 Original Lacrado",
        "price": 120.00,
        "seller": "HP-Store-Oficial",
        "description": "Cartucho lacrado, selo de garantia, compatível com HP DeskJet.",
        "positive_occurrences": 1,
        "negative_occurrences": 0,
        "label": "original"
    },
    {
        "title": "Cartucho HP 65 Super Barato Genérico",
        "price": 15.90,
        "seller": "lojinha123",
        "description": "Cartucho para impressora HP, mas sem selo de garantia, descrição com erros ortográficos.",
        "positive_occurrences": 0,
        "negative_occurrences": 0,
        "label": "suspeito"
    }
]

def build_message(record):
    # Monta a parte user do chat com o exemplo + caso real
    examples = ""
    for ex in FEW_SHOT_EXAMPLES:
        examples += (
            f"Título: {ex['title']}\n"
            f"Preço: R$ {ex['price']:.2f}\n"
            f"Vendedor: {ex['seller']}\n"
            f"Descrição: {ex['description']}\n"
            f"Ocorrências positivas nos comentários: {ex['positive_occurrences']}\n"
            f"Ocorrências negativas nos comentários: {ex['negative_occurrences']}\n"      
            f"Classificação: {ex['label']}\n\n"
        )
    # agora o item real
    examples += (
        f"Título: {record['title']}\n"
        f"Preço: R$ {record['price']:.2f}\n"
        f"Vendedor: {record['seller']}\n"
        f"Descrição: {record['description']}\n"
        f"Ocorrências positivas nos comentários: {record['positive_occurrences']}\n"
        f"Ocorrências negativas nos comentários: {record['negative_occurrences']}\n"
        "Classificação:"
    )
    return examples

def classify_and_update(db_path="mercadolivre.db", rate_limit_sec=1.5):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 3) Busca itens sem label
    cur.execute("""
        SELECT id, title, price, seller, description, positive_occurrences, negative_occurrences
        FROM products_data
        WHERE label IS NULL
    """)
    rows = cur.fetchall()

    for row in rows:
        rec = {
            "id":                    row[0],
            "title":                 row[1],
            "price":                 row[2],
            "seller":                row[3] or "",
            "description":           row[4] or "",
            "positive_occurrences": row[5],
            "negative_occurrences": row[6]
        }

        try:
            # 4) Chamada à API
            res = client.responses.create(
                model="gpt-4o-mini",
                instructions=(
                    SYSTEM_PROMPT  
                ),
                input=build_message(rec)  
            )
            label = res.output_text.strip().lower()

            if label not in ("original", "suspeito"):
                label = "suspeito"

            # 5) Atualiza DB
            cur.execute(
                "UPDATE products_data SET label = ? WHERE id = ?",
                (label, rec["id"])
            )
            conn.commit()
            print(f"[ID {rec['id']}] → {label}")

        except Exception as e:
            print(f"Erro no ID {rec['id']}: {e}")

        time.sleep(rate_limit_sec)  # controla taxa de requisições

    conn.close()
