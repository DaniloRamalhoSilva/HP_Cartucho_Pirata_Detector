import os
import json
import sqlite3
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI


# 1) Configure sua API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
Você recebe o HTML bruto de uma página de anúncio de cartucho HP. Retorne um JSON com os campos:
- marca: (ex: HP)
- modelo: (ex: 65)
- preco: número (ex: 120.00)
- cor: (ex: preto, colorido)
- qualidade_descricao: breve avaliação da clareza/ortografia do texto (ex: \"boa\", \"média\", \"ruim\")
- quantidade_reviews: inteiro
- quantidade_fotos: inteiro
- classificacao_confianca: procure elementos que possam identificar se o produto é "Original", "Pirata" ou "Suspeito"
Responda **somente** com um JSON válido.
"""

def extract_structured(html: str) -> dict:

    res = client.responses.create(
        model="gpt-4o-mini",
        instructions=(
            SYSTEM_PROMPT  
        ),
        input=html  
    )
    content = res.output_text.strip().lower()
    
    # Remove blocos markdown
    if content.startswith("```json"):
        content = content.replace("```json", "").strip()
    if content.endswith("```"):
        content = content[:-3].strip()

    return json.loads(content)

def process_all_html():
    conn = sqlite3.connect("mercadolivre.db")
    cur = conn.cursor()

    # busca todas as páginas ainda não processadas
    cur.execute("""
        SELECT id, products_data_id, raw_html 
          FROM products_html_raw 
         WHERE processed = 0      
    """)
    rows = cur.fetchall()

    for raw_id, pdid, html in rows:
        try:
            
            data = extract_structured(html)

            # insere na tabela estruturada
            cur.execute("""
                INSERT INTO products_structured_llm
                  (products_data_id, marca, modelo, preco, cor,
                   qualidade_descricao, quantidade_reviews, quantidade_fotos, classificacao_confianca)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                pdid,
                data.get("marca"),
                data.get("modelo"),
                data.get("preco"),
                data.get("cor"),
                data.get("qualidade_descricao"),
                data.get("quantidade_reviews"),
                data.get("quantidade_fotos"),
                data.get("classificacao_confianca")
            ))
            # marca como processado
            cur.execute(
                "UPDATE products_html_raw SET processed = 1 WHERE id = ?",
                (raw_id,)
            )
            conn.commit()
        except Exception as e:
            print(f"Erro ao processar HTML {raw_id}: {e}")

    # exporta CSV com tudo que foi extraído
    df = pd.read_sql("""
        SELECT u.produto, s.*
          FROM products_structured_llm s
          JOIN products_url u
            ON s.products_data_id = u.id
    """, conn)
    df.to_csv("structured_data.csv", index=False, sep=";")

    conn.close()

if __name__ == "__main__":
    #process_all_html()
    html_fake = """
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <title>Cartucho HP 65 Preto Original</title>
        </head>
        <body>
            <div class="produto">
                <h1>Cartucho de Tinta HP 65 - Preto</h1>
                <p class="marca">Marca: <strong>HP</strong></p>
                <p class="modelo">Modelo: <strong>65</strong></p>
                <p class="preco">Preço: <strong>R$ 120,00</strong></p>
                <p class="cor">Cor: <strong>Preto</strong></p>
                <p class="descricao">Descrição: Cartucho original de alta qualidade, com excelente rendimento e impressão nítida.</p>
                <p class="qualidade">Qualidade do texto: <strong>boa</strong></p>
                <p class="reviews">Avaliações de clientes: <strong>245</strong> reviews</p>
                <div class="galeria-fotos">
                    <p>Imagens do produto: <strong>3</strong> fotos disponíveis</p>
                    <img src="foto1.jpg" alt="Foto 1">
                    <img src="foto2.jpg" alt="Foto 2">
                    <img src="foto3.jpg" alt="Foto 3">
                </div>
                <div class="confianca">
                    <p>Autenticidade: <span style="color: green;"><strong>Produto Original</strong></span></p>
                </div>
            </div>
        </body>
        </html>
    """

    process_all_html()
    print("Extração estruturada concluída e CSV gerado.")
