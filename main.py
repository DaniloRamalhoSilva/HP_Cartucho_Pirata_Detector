from database import save_product
from mercadolivre import scrap_list, scrap_product, scrap_comments
from classifier import classify_and_update
from utils import export_dataset, update_comment_counts

from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.options import Options

import time, random
import database

def list(produto, driver, limit = 5):
    url = f"https://lista.mercadolivre.com.br/{quote(produto)}"
    page = scrap_list(produto, url, driver)

    counter = 0
    while page and counter < limit:
        counter = counter + 1
        page = scrap_list(produto, page, driver)
        time.sleep(random.uniform(2.0, 3.0))  # para evitar ser identificado como scrap]

def product(driver, limit = 10):
    products_url = database.query(f"select * from products_url limit {limit}")

    for product_url in products_url:
        try:
            print(product_url[2])
            url, title, price, product_review_rating, product_review_amount, seller, description = scrap_product(product_url[2], driver)
            save_product(product_url[0], url, title, price, product_review_rating, product_review_amount, seller, description)
            database.query(f"update products_url set scraped = 1 where id = {product_url[0]}")
        except Exception as e:
            print(e)
            continue

def comments(driver, limit = None, comments_limit = 0):
    if limit:
        limit = f"limit {limit}"

    products_data = database.query(f"select * from products_data {limit}")
    for product_data in products_data:
        print(product_data[2])
        scrap_comments(product_data[0], product_data[2], comments_limit, driver)


if __name__ == "__main__":
    # criando tabelas caso não existam
    database.create_db()

    #criando driver
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    
    # Configuração de Script 
    produto = "cartucho hp 667 preto"
    paginas = 1
    produtos = 50
    comentarios = 10

    # Scraping
    list(produto, driver, paginas)
    product(driver, produtos)
    comments(driver, produtos, comentarios)

    # Crai uma pontuação para comentarios positivos e negativos
    update_comment_counts()

    # executa classificação e grava no SQLite
    classify_and_update()   

    # Crai o dataset em csv
    export_dataset() 

