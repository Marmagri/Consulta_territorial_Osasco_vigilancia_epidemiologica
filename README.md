# Consulta_territorial_Osasco_vigilancia_epidemiologica
Aplicação em Python (Streamlit) para consulta territorial em saúde no município de Osasco. Permite identificar UBS de referência, setor censitário e bairro IBGE a partir de CEP ou endereço, integrando dados geográficos e administrativos para apoiar ações da Vigilância Epidemiológica.


# 🗺️ Consulta Territorial em Saúde – Osasco

Aplicação desenvolvida em Python (Streamlit) para apoio à Vigilância Epidemiológica do município de Osasco.

A ferramenta permite identificar, a partir de um CEP ou endereço:

* Unidade Básica de Saúde (UBS) de referência
* Setor censitário (IBGE)
* Bairro oficial (IBGE)

O objetivo é integrar diferentes bases territoriais e facilitar a tomada de decisão em ações de saúde pública, especialmente no contexto de arboviroses como a dengue.

---

## 🚀 Funcionalidades

* 🔎 Busca por CEP ou logradouro (com suporte a campos opcionais)
* 📍 Retorno automático da UBS correspondente
* 🧭 Identificação do setor censitário via geoprocessamento
* 🏙️ Identificação do bairro IBGE
* 🗺️ Visualização interativa em mapa (Folium)

---

## 🧠 Tecnologias utilizadas

* Python
* Streamlit
* Pandas
* GeoPandas
* Shapely
* Folium

---

## 📊 Fontes de dados

* Setores censitários e bairros: IBGE (Censo 2022)
* Base de logradouros com coordenadas: uso interno da Prefeitura de Osasco

---

## 🔒 Sobre os dados

Este repositório **não inclui a base completa de logradouros e vínculos com UBS**, pois contém informações de uso interno da administração municipal.

A estrutura do projeto foi mantida de forma que os dados possam ser facilmente integrados localmente, respeitando princípios de segurança da informação e governança de dados públicos.

Os arquivos geoespaciais do IBGE podem ser obtidos publicamente no site oficial:
(https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/26565-malhas-de-setores-censitarios-divisoes-intramunicipais.html)

---

## 📁 Estrutura do projeto

```
mapa-ubs-osasco/
│
├── app/
│   └── Mapa_CEP_Osasco.py
│
└── requirements.txt
```

---

## ▶️ Como executar

1. Instale as dependências:

```
pip install -r requirements.txt
```

2. Execute a aplicação:

```
streamlit run app/Mapa_CEP_Osasco.py
```

---

## 🎯 Contexto de uso

Este projeto foi desenvolvido no contexto da Vigilância Epidemiológica municipal, com foco na integração de dados territoriais para:

* Planejamento de ações de controle de dengue
* Apoio à análise espacial
* Organização da rede de atenção básica

---

## 👩‍💻 Autora

Marta Motter Magri
Vigilância Epidemiológica – Prefeitura de Osasco

---

## 📌 Observação

Este projeto representa uma iniciativa prática de aplicação de ciência de dados e geoprocessamento no setor público, podendo ser adaptado para outros municípios e contextos.
