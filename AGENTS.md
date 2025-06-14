Challenge Sprint - HP

# Sprint 1 (FINALIZADO): Coleta e Construção da Base de Dados 

A empresa HP deseja identificar possíveis casos de pirataria de seus produtos vendidos em sites de e-commerce. Anúncios com preços muito abaixo do praticado oficialmente podem indicar falsificações. O objetivo do projeto é desenvolver uma solução inteligente e automatizada, com Web Scraping, Análise de Dados, Machine Learning e Deploy em WebApp que ajude na identificação de produtos suspeitos.  

Como  1º Entregável da disciplina Front End & Mobile Development o(a) aluno(a) deverá criar uma dataset através da coleta de dados em anúncios de produtos da marca, extraídos de sites de e-commerce, contendo informações úteis para posterior análise e classificação.  

Realizar Web Scraping de plataformas de e-commerce (Ex: Mercado Livre, OLX, Shopee, Amazon).  

Coletar dados como:
- Título do anúncio
- Preço
- Descrição
- Nome do vendedor
- Avaliações (se houver)
- Link do anúncio

Criar critérios heurísticos iniciais para rotular os dados como:
"original" (baseado em lojas oficiais, preço médio coerente, verificado, etc.)  
"suspeito/pirata" (preço abaixo da média, loja desconhecida, erros de gramática, etc.)  

Gerar um dataset estruturado, com features relevantes e feature target de rótulo binário (original / pirata).  

Preparar uma apresentação documentando as fontes e decisões tomadas no processo de scraping e rotulagem. Incluir a descrição (nome) das features coletadas e 5 exemplos de amostras de dados.  


# Sprint 2 (EM ANDAMENTO): Análise Exploratória e Descritiva dos Dados 

Realizar EDA (Análise de Dados Exploratória) na base coletada.

Definir escopo do projeto (segmento de produtos, abrangência de sites, etc)

Analisar: 
- distribuição dos preços
- frequência de palavras nos títulos/descrições (wordclouds, n-grams)
- correlações entre variáveis
- distribuição dos anúncios por rótulo
- identificar possíveis features úteis para modelagem (ex: presença de determinadas palavras, faixas de preço, tipo de vendedor).

**Entregar notebook (ipynb), contendo:**

Limpeza da base;
EDA (Análise Exploratória de Dado);
Comentários;
Extra: cronograma macro do projeto seguindo as etapas da metodologia CRISP-DM;

Subir arquivo PDF ou txt diretamente no portal Fiap, na seção de Entrega de Trabalhos, contendo link do repositório Github.


**Todos os commits em portugues!**