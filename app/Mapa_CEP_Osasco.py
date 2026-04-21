import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("Consulta Territorial – Osasco")
st.markdown("Digite um CEP ou selecione um endereço para identificar UBS, setor censitário e bairro.")

#1 CAMINHOS
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CAMINHO_SETORES = os.path.join(BASE_DIR, "data", "SP_setores_CD2022.shp")
CAMINHO_BAIRROS = os.path.join(BASE_DIR, "data", "SP_bairros_CD2022.shp")
CAMINHO_BASE = os.path.join(BASE_DIR, "data", "Coordenadas.xlsx")

#2 CARREGAR DADOS

@st.cache_data
def carregar_dados():

    # Verificação de arquivos
    if not os.path.exists(CAMINHO_SETORES):
        st.error("Arquivo de setores não encontrado.")
        return None, None, None

    if not os.path.exists(CAMINHO_BAIRROS):
        st.error("Arquivo de bairros não encontrado.")
        return None, None, None

    if not os.path.exists(CAMINHO_BASE):
        st.error("Arquivo Coordenadas.xlsx não encontrado.")
        return None, None, None

    setores = gpd.read_file(CAMINHO_SETORES)
    bairros = gpd.read_file(CAMINHO_BAIRROS)

    setores = setores[setores["NM_MUN"].str.upper() == "OSASCO"]
    bairros = bairros[bairros["NM_MUN"].str.upper() == "OSASCO"]

    setores = setores.to_crs("EPSG:4326")
    bairros = bairros.to_crs("EPSG:4326")

    base = pd.read_excel(CAMINHO_BASE)

    # Ajuste coordenadas
    base["x"] = base["x"].astype(str).str.replace(",", ".").astype(float)
    base["y"] = base["y"].astype(str).str.replace(",", ".").astype(float)

    # Limpeza CEP
    base["cep"] = (
        base["cep"]
        .astype(str)
        .str.replace("-", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.strip()
    )

    return setores, bairros, base


setores, bairros, base = carregar_dados()

# Se deu erro no carregamento, parar execução
if setores is None:
    st.stop()


#3 CONTROLE DE ESTADO


if "resultado" not in st.session_state:
    st.session_state.resultado = None

if "logradouro" not in st.session_state:
    st.session_state.logradouro = ""

if "cep" not in st.session_state:
    st.session_state.cep = ""

#FUNÇÃO CORRETA PARA LIMPAR
def limpar_busca():
    st.session_state["logradouro"] = ""
    st.session_state["cep"] = ""
    st.session_state["resultado"] = None


#4 BUSCA


st.subheader("Buscar endereço ou CEP")

col1, col2 = st.columns(2)

with col1:
    lista_enderecos = [""] + sorted(base["logradouro"].dropna().unique().tolist())

    st.selectbox(
        "Selecione o endereço (opcional):",
        lista_enderecos,
        key="logradouro"
    )

with col2:
    st.text_input(
        "Ou digite o CEP (somente números):",
        key="cep"
    )

col3, col4 = st.columns(2)

with col3:
    consultar = st.button("Consultar")

with col4:
    st.button("Limpar Busca", on_click=limpar_busca)

#5 CONSULTA


if consultar:

    cep_digitado = (
        st.session_state.cep.replace("-", "")
        .replace(".", "")
        .strip()
    )

    if cep_digitado != "":
        filtro = base[base["cep"] == cep_digitado]
        if not filtro.empty:
            st.session_state.resultado = filtro.iloc[0]
        else:
            st.error("CEP não encontrado.")
            st.session_state.resultado = None

    elif st.session_state.logradouro != "":
        filtro = base[base["logradouro"] == st.session_state.logradouro]
        if not filtro.empty:
            st.session_state.resultado = filtro.iloc[0]
        else:
            st.error("Endereço não encontrado.")
            st.session_state.resultado = None

    else:
        st.warning("Informe um CEP ou selecione um endereço.")

#6 RESULTADO


if st.session_state.resultado is not None:

    resultado = st.session_state.resultado

    st.markdown("---")
    st.subheader("Resultado da Consulta")

    st.write("UBS:", resultado["UNIDADE"])
    st.write("Endereço:", resultado["logradouro"])
    st.write("CEP:", resultado["cep"])

    ponto = gpd.GeoDataFrame(
        [resultado],
        geometry=[Point(resultado["x"], resultado["y"])],
        crs="EPSG:4326"
    )

    setor_join = gpd.sjoin(ponto, setores, how="left", predicate="within")
    bairro_join = gpd.sjoin(ponto, bairros, how="left", predicate="within")

    coluna_setor = [col for col in setor_join.columns if "CD_SETOR" in col]
    coluna_bairro = [col for col in bairro_join.columns if "NM_BAIRRO" in col]

    if coluna_setor and pd.notna(setor_join.iloc[0][coluna_setor[0]]):
        st.write("Setor Censitário:", setor_join.iloc[0][coluna_setor[0]])
    else:
        st.write("Setor Censitário: Não encontrado")

    if coluna_bairro and pd.notna(bairro_join.iloc[0][coluna_bairro[0]]):
        st.write("Bairro IBGE:", bairro_join.iloc[0][coluna_bairro[0]])
    else:
        st.write("Bairro IBGE: Não encontrado")

    m = folium.Map(
        location=[resultado["y"], resultado["x"]],
        zoom_start=16
    )

    folium.Marker(
        location=[resultado["y"], resultado["x"]],
        popup=f"UBS: {resultado['UNIDADE']}",
        tooltip="Local pesquisado",
        icon=folium.Icon(color="red")
    ).add_to(m)

    st_folium(m, width=1000, height=600)

else:
    st.info("Preencha os campos e clique em Consultar.")
