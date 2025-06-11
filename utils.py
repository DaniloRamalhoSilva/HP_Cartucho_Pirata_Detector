import sqlite3
import re
import pandas as pd

NEGATIVAS = [
    r"\bfalso\b",                  # falso
    r"\bfalsificado\b",            # falsificado
    r"\bpirata\b",                 # pirata
    r"não[ée] original",           # cobre “não é original” e “não e original”
    r"\bgeneric[oa]\b",            # genérico / generica
    r"\bdefeituoso\b",             # defeituoso
    r"\bdefeito\b",                # defeito
    r"\bquebrou\b",                # quebrou
    r"\bimita(?:ção|[ãa]o)\b",     # imitação / imitacao
    r"\bcontrafeito\b",            # contrafeito
    r"\bsem garantia\b",           # sem garantia
    r"\bdecepç(?:ão|oes)\b",       # decepção / decepcoes
    r"\barrependid[oa]\b",         # arrependido/a
    r"\binsatisfeit[oa]\b",        # insatisfeito/a
    r"\bproduto ruim\b",           # produto ruim

]

POSITIVAS = [
    r"produto original",           # produto original
    r"\bótima qualidade\b",        # ótima qualidade
    r"\bexcelente produto\b",      # excelente produto
    r"\bfuncionou bem\b",          # funcionou bem
    r"\brecomendo\b",              # recomendo
    r"\bsatisfeit[oa]\b",          # satisfeito/a
    r"\bgarantia\b",               # garantia
    r"\bmuito bom\b",              # muito bom
    r"\bperfeito\b",               # perfeito
]


def update_comment_counts(db_path="mercadolivre.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # para cada produto em products_data
    cur.execute("SELECT id FROM products_data")
    ids = [row[0] for row in cur.fetchall()]

    for pid in ids:
        # pega todos os reviews do produto
        cur.execute("SELECT review FROM products_review WHERE products_data_id = ?", (pid,))
        reviews = [r[0].lower() for r in cur.fetchall()]

        pos = neg = 0
        for text in reviews:
            for p in POSITIVAS:
                pos += len(re.findall(p, text))
            for n in NEGATIVAS:
                neg += len(re.findall(n, text))

        # atualiza no banco
        cur.execute("""
            UPDATE products_data
            SET positive_occurrences = ?, negative_occurrences = ?
            WHERE id = ?
        """, (pos, neg, pid))

    conn.commit()
    conn.close()


def export_dataset():
    conn = sqlite3.connect("mercadolivre.db")
    df = pd.read_sql("""
        SELECT id, label, positive_occurrences, negative_occurrences, 
               price, review_rating, url, title, review_amount, seller,
               description, url, data_cadastro
        FROM products_data  
    """, conn)
    df.to_csv("data\dataset_hp.csv", index=False, sep=";")

