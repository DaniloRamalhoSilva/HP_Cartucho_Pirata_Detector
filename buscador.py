from webscrap import webscraping
from urllib.parse import quote, quote_plus


def buscar(produto):
    """
        Realiza uma busca de produtos no site Mercado Livre com base no termo fornecido.

        Args:
            produto (str): O termo de busca que será utilizado para pesquisar produtos.

        Returns:
            list[dict]: Uma lista de dicionários contendo as informações dos produtos encontrados:
                - "termo_de_busca" (str): O termo utilizado na busca.
                - "titulo_produto" (str): O título do produto encontrado.
                - "preço" (str): O preço do produto.
                - "link" (str): O link para a página do produto.
        """
    try:
        produtos_encontrados = []
        produto_formatado = quote(produto)

        url = f"https://lista.mercadolivre.com.br/{produto_formatado}"
        print(url)

        # Faz o webscraping
        resultado = webscraping(url)

        if resultado:

            ol_elements = definir_tipo_grid(resultado)

            if ol_elements:
                # Encontra todos os elementos li dentro do ol
                li_elements = ol_elements.find_all('li', class_='ui-search-layout__item')

                print(f"Total de itens encontrados: {len(li_elements)}")

                # Exibe cada item encontrado
                for index, li in enumerate(li_elements, 1):

                    # Encontra o link dentro do elemento li
                    link = li.find('a', class_='poly-component__title')
                    price = li.find('div', class_='poly-price__current')
                    real = price.find('span', class_='andes-money-amount__fraction')
                    centavos = price.find('span',
                                          class_='andes-money-amount__cents andes-money-amount__cents--superscript-24')

                    if link:
                        # Extrai o href do link
                        href = link.get('href')
                        title = link.text

                    if centavos:
                        current_price = f"{real.text}.{centavos.text}"
                    else:
                        current_price = f"{real.text}.00"

                    produtos_encontrados.append({"termo_de_busca": produto, "titulo_produto": title, "preço": current_price, "link": href})
                    #print(f"{index} - {title} - {current_price} - {href}")
            else:
                print("Não foi possível encontrar a lista de produtos.")

        return produtos_encontrados

    except Exception as e:
        print(f"Ocorreu um erro ao buscar produto: {e}")

def definir_tipo_grid(resultado):
    """
        Identifica o tipo de layout (grid ou stack) da listagem de produtos em uma página de resultados.

        Args:
            resultado (BeautifulSoup): O conteúdo HTML da página, parseado com BeautifulSoup.

        Returns:
            Tag or None: Retorna a tag `<ol>` correspondente ao layout encontrado (grid ou stack),
            ou `None` caso nenhum dos layouts seja identificado.
    """

    try:
        # Encontra a tag ol com a classe específica
        grid = resultado.find('ol', class_='ui-search-layout ui-search-layout--grid')

        #se não for do tipo grid tentamos do tipo stack
        if grid:
            return grid

        stack = resultado.find('ol', class_='ui-search-layout ui-search-layout--stack')
        if stack:
            return stack

        return None

    except Exception as e:
        print(f"Ocorreu um erro ao tentar recuperar o grid {e}")

