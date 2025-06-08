import sqlite3

def create_db():
    """
    Cria o banco de dados SQLite com três tabelas:
    - products_url: Armazena URLs de produtos para scraping
    - products_data: Armazena dados gerais dos produtos
    - products_review: Armazena avaliações dos produtos
    - products_html_raw Armazena HTML bruto
    - products_structured_llm Armazena dados estruturados extraídos de uma ferramenta de LLM
    """
    conn = sqlite3.connect("mercadolivre.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products_url (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT,
            url TEXT,
            scraped INTEGER DEFAULT 0,
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            products_url_id INTEGER,
            url TEXT,
            title TEXT,
            price REAL,
            review_rating REAL,
            review_amount INTEGER,
            seller TEXT,
            description TEXT,
            comments_scraped INTEGER DEFAULT 0,
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
            positive_occurrences INTEGER DEFAULT 0,
            negative_occurrences occurrences INTEGER DEFAULT 0,    
            label TEXT DEFAULT NULL    
        )
    """)
    conn.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products_review (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            products_data_id INTEGER,
            rating INTEGER,
            review TEXT,
            review_date text,
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products_html_raw (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        products_data_id INTEGER,
        raw_html TEXT,
        processed INTEGER DEFAULT 0,
        data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products_structured_llm (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        products_data_id INTEGER,
        marca TEXT,
        modelo TEXT,
        preco REAL,
        cor TEXT,
        qualidade_descricao TEXT,
        quantidade_reviews INTEGER,
        quantidade_fotos INTEGER,
        classificacao_confianca TEXT,
        data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()

    conn.close()


def save_url(produto, url):
    """
    Salva um novo produto e sua URL na tabela products_url.

    Args:
        produto (str): Nome do produto
        url (str): URL do produto no Mercado Livre
    """
    conn = sqlite3.connect("mercadolivre.db")
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO products_url (produto, url) VALUES (?, ?)", (produto, url))
        conn.commit()
    except Exception as e:
        print(f"Erro ao inserir produto, url: {e}")
    finally:
        conn.close()

def save_product(products_url_id, url, title, price, review_rating, review_amount, seller, description):
    """
    Salva os dados de um produto na tabela products_data.

    Args:
        product_url_id (id): id da tabela products_url
        url (str): URL do produto
        title (str): Título do produto
        price (float): Preço do produto
        review_rating (float): Média das avaliações
        review_amount (int): Quantidade de avaliações
        seller (str): Nome do vendedor
        description (str): Descrição do produto
    """
    conn = sqlite3.connect("mercadolivre.db")
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO products_data (products_url_id, url, title, price, review_rating, review_amount, seller, description)"
                    "values (?, ?, ?, ?, ?, ?, ?, ?) ",
            (products_url_id, url, title, price, review_rating, review_amount, seller, description))
        conn.commit()
    except Exception as e:
        print(f"Erro ao inserir produto, url: {e}")
    finally:
        conn.close()

def save_review(products_data_id, rating, review, review_date):
    """
    Salva uma avaliação de produto na tabela products_review.

    Args:
        products_data_id (int): ID do produto relacionado
        rating (int): Nota da avaliação
        review (str): Texto da avaliação
        review_date (str): Data da avaliação
    """
    conn = sqlite3.connect("mercadolivre.db")
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO products_review (products_data_id, rating, review, review_date)values (?, ?, ?, ?) ", (products_data_id, rating, review, review_date))
        conn.commit()
    except Exception as e:
        print(f"Erro ao inserir produto, url: {e}")
    finally:
        conn.close()

def save_raw_html(products_data_id: int, html: str):
    conn = sqlite3.connect("mercadolivre.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products_html_raw (products_data_id, raw_html) VALUES (?, ?)",
        (products_data_id, html)
    )
    conn.commit()
    conn.close()

def query(sql):
    """
    Executa uma consulta SQL personalizada no banco de dados.

    Args:
        sql (str): Query SQL a ser executada

    Returns:
        list: Resultado da consulta em forma de lista
    """
    conn = sqlite3.connect("mercadolivre.db")
    try:
        query = sql.split(' ')
        cur = conn.cursor()
        cur.execute(sql)

        if query[0].lower() == "select":
            return cur.fetchall()
        else:
            conn.commit()
            return True

    except Exception as e:
      print(f"Erro ao tentar executar a query: {e}")
    finally:
        conn.close()
        
