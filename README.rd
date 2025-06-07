# HP Cartucho Pirata Detector 🕵️‍♂️📦

Bem-vindo ao projeto **HP Cartucho Pirata Detector**, uma solução completa para coleta, análise e classificação de anúncios de cartuchos HP em marketplaces, auxiliando a identificação de produtos suspeitos de pirataria.

---

## 🚀 Visão Geral

Este repositório implementa um pipeline automatizado para:

1. **Scraping** de anúncios no Mercado Livre.
2. **Armazenamento** dos dados em banco SQLite.
3. **Análise de comentários** via regex para extrair evidências quantitativas.
4. **Classificação** binária (`original` vs. `suspeito`) usando LLM (OpenAI GPT).  

O resultado é um dataset pronto para EDA ou integração em sistemas de monitoramento de e-commerce.

---

## 📋 Funcionalidades Principais

- **Coleta de URLs**: navega e pagina listagens de produtos.
- **Extração de dados**: título, preço, avaliações, vendedor e descrição.
- **Comentários**: coleta e armazena reviews, com limite configurável.
- **Evidências via Regex**: conta ocorrências de termos positivos e negativos nos comentários.
- **Classificação LLM**: prompt few-shot com GPT para decidir `original`/`suspeito`.
- **Banco de Dados**: estrutura normalizada em SQLite para consultas e exportação.

---

## 📦 Pré-requisitos

- Python 3.10+  
- Google Chrome instalado

**Bibliotecas Python** (exemplo `requirements.txt`):
```txt
selenium
openai
pandas
python-dotenv
```

Instalação rápida:
```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuração do Ambiente

**1. Clone o repositório:**
```bash
git clone https://github.com/SeuUsuario/hp-cartucho-detector.git
cd hp-cartucho-detector
```
**2. Crie e ative um ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venvScriptsactivate     # Windows
```
**3. Instale dependências:**
```bash
pip install -r requirements.txt
```
**4. Configure sua chave OpenAI (no `.env`):**
```env
OPENAI_API_KEY=sk-...
```

---

## 💻 Estrutura do Projeto

```
├── main.py              # Script principal: orquestra scraping e classificação
├── classifier.py        # Lógica de prompt GPT e atualização de labels
├── database.py          # Criação/alteração do esquema SQLite e funções de CRUD
├── mercadolivre.py      # Funções de scraping de listagem, produto e comentários
├── utils.py             # Contagem de regex e helpers
├── docs/ 
│   └── dataset_hp.csv   # Dados em CSV
├── docs/                # Documentação e exemplos de amostras
│   └── Relatorio - Coleta e Construção da Base de Dados.docx   # Documentação completa do Entregável 1
├── requirements.txt     # Dependências do Python
├── README.md            # Este arquivo
└── mercadolivre.db      # Banco de dados SQLite (gerado em runtime)
```

---

## 🛠️ Como Usar

```bash
python main.py
```
---


## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo \`LICENSE\` para mais detalhes.

---

## 👨‍🏫 Autores:
- Danilo Ramalho Silva | RM: 555183
- Israel Dalcin Alves Diniz | RM: 554668
- João Vitor Pires da Silva | RM: 556213
- Matheus Hungaro | RM: 555677
- Pablo Menezes Barreto | RM: 556389
- Tiago Toshio Kumagai Gibo | 556984