import streamlit as st
import sqlite3
from datetime import date

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Controle de Produção Acadêmica",
    page_icon="📚",
    layout="wide"
)

DB = "academia.db"


# ============================================================
# BANCO DE DADOS
# ============================================================

def conectar():
    return sqlite3.connect(DB)


def criar_banco():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artigos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autores TEXT,
            tema TEXT,
            status TEXT,
            progresso INTEGER DEFAULT 0,
            prazo TEXT,
            observacoes TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projetos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            problema TEXT,
            hipotese TEXT,
            objetivo TEXT,
            palavras_chave TEXT,
            status TEXT,
            observacoes TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS periodicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            issn TEXT,
            qualis TEXT,
            area TEXT,
            scopus TEXT,
            web_of_science TEXT,
            scielo TEXT,
            site TEXT,
            observacoes TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artigo TEXT NOT NULL,
            periodico TEXT NOT NULL,
            data_submissao TEXT,
            status TEXT,
            prazo TEXT,
            observacoes TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS publicacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artigo TEXT NOT NULL,
            periodico TEXT,
            doi TEXT,
            data_publicacao TEXT,
            link TEXT,
            observacoes TEXT
        )
    """)

    conn.commit()
    conn.close()


criar_banco()


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def inserir(tabela, campos, valores):
    conn = conectar()
    cursor = conn.cursor()

    placeholders = ", ".join(["?"] * len(valores))
    campos_sql = ", ".join(campos)

    cursor.execute(
        f"INSERT INTO {tabela} ({campos_sql}) VALUES ({placeholders})",
        valores
    )

    conn.commit()
    conn.close()


def buscar(tabela):
    conn = conectar()

    dados = conn.execute(
        f"SELECT * FROM {tabela}"
    ).fetchall()

    colunas = [
        descricao[0]
        for descricao in conn.execute(
            f"PRAGMA table_info({tabela})"
        ).fetchall()
    ]

    conn.close()

    return dados, colunas


def excluir(tabela, registro_id):
    conn = conectar()
    conn.execute(
        f"DELETE FROM {tabela} WHERE id = ?",
        (registro_id,)
    )
    conn.commit()
    conn.close()


def quantidade(tabela):
    conn = conectar()
    resultado = conn.execute(
        f"SELECT COUNT(*) FROM {tabela}"
    ).fetchone()[0]
    conn.close()
    return resultado


# ============================================================
# MENU
# ============================================================

st.sidebar.title("📚 Produção Acadêmica")

pagina = st.sidebar.radio(
    "Navegação",
    [
        "Dashboard",
        "Artigos",
        "Projetos",
        "Periódicos",
        "Submissões",
        "Publicações"
    ]
)

st.sidebar.divider()

st.sidebar.caption("Controle de Produção Acadêmica")
st.sidebar.caption("Versão 1.0")


# ============================================================
# DASHBOARD
# ============================================================

if pagina == "Dashboard":

    st.title("📊 Dashboard")

    st.write(
        "Visão geral da sua produção científica."
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Artigos",
        quantidade("artigos")
    )

    col2.metric(
        "Projetos",
        quantidade("projetos")
    )

    col3.metric(
        "Periódicos",
        quantidade("periodicos")
    )

    col4.metric(
        "Submissões",
        quantidade("submissoes")
    )

    col5.metric(
        "Publicações",
        quantidade("publicacoes")
    )

    st.divider()

    artigos, _ = buscar("artigos")

    if artigos:

        st.subheader("Artigos em andamento")

        for artigo in artigos:

            (
                id_artigo,
                titulo,
                autores,
                tema,
                status,
                progresso,
                prazo,
                observacoes
            ) = artigo

            col1, col2 = st.columns([4, 1])

            with col1:
                st.write(f"**{titulo}**")

                if autores:
                    st.caption(f"Autores: {autores}")

                if tema:
                    st.caption(f"Tema: {tema}")

            with col2:
                st.progress(
                    min(max(progresso, 0), 100) / 100
                )
                st.caption(f"{progresso}% concluído")

            st.divider()

    else:

        st.info(
            "Ainda não há artigos cadastrados."
        )


# ============================================================
# ARTIGOS
# ============================================================

elif pagina == "Artigos":

    st.title("📝 Artigos em andamento")

    aba1, aba2 = st.tabs(
        ["Cadastrar artigo", "Artigos cadastrados"]
    )

    with aba1:

        with st.form("form_artigo"):

            titulo = st.text_input(
                "Título"
            )

            autores = st.text_input(
                "Autores"
            )

            tema = st.text_input(
                "Tema"
            )

            status = st.selectbox(
                "Status",
                [
                    "Ideia",
                    "Pesquisa bibliográfica",
                    "Metodologia",
                    "Redação",
                    "Revisão",
                    "Finalização",
                    "Pronto para submissão"
                ]
            )

            progresso = st.slider(
                "Percentual de conclusão",
                0,
                100,
                0
            )

            prazo = st.date_input(
                "Prazo",
                value=None
            )

            observacoes = st.text_area(
                "Observações"
            )

            enviar = st.form_submit_button(
                "Cadastrar artigo"
            )

            if enviar:

                if not titulo:
                    st.error(
                        "Informe o título do artigo."
                    )

                else:

                    inserir(
                        "artigos",
                        [
                            "titulo",
                            "autores",
                            "tema",
                            "status",
                            "progresso",
                            "prazo",
                            "observacoes"
                        ],
                        [
                            titulo,
                            autores,
                            tema,
                            status,
                            progresso,
                            str(prazo),
                            observacoes
                        ]
                    )

                    st.success(
                        "Artigo cadastrado com sucesso."
                    )

    with aba2:

        dados, _ = buscar("artigos")

        if not dados:

            st.info(
                "Nenhum artigo cadastrado."
            )

        for artigo in dados:

            (
                id_artigo,
                titulo,
                autores,
                tema,
                status,
                progresso,
                prazo,
                observacoes
            ) = artigo

            with st.expander(titulo):

                st.write(f"**Autores:** {autores}")
                st.write(f"**Tema:** {tema}")
                st.write(f"**Status:** {status}")
                st.progress(progresso / 100)
                st.write(f"**Conclusão:** {progresso}%")
                st.write(f"**Prazo:** {prazo}")

                if observacoes:
                    st.write(
                        f"**Observações:** {observacoes}"
                    )

                if st.button(
                    "Excluir artigo",
                    key=f"excluir_artigo_{id_artigo}"
                ):

                    excluir(
                        "artigos",
                        id_artigo
                    )

                    st.rerun()


# ============================================================
# PROJETOS
# ============================================================

elif pagina == "Projetos":

    st.title("💡 Projetos de artigos")

    aba1, aba2 = st.tabs(
        ["Novo projeto", "Projetos cadastrados"]
    )

    with aba1:

        with st.form("form_projeto"):

            titulo = st.text_input(
                "Título provisório"
            )

            problema = st.text_area(
                "Problema de pesquisa"
            )

            hipotese = st.text_area(
                "Hipótese"
            )

            objetivo = st.text_area(
                "Objetivo geral"
            )

            palavras_chave = st.text_input(
                "Palavras-chave"
            )

            status = st.selectbox(
                "Status",
                [
                    "Ideia",
                    "Em desenvolvimento",
                    "Projeto definido",
                    "Transformar em artigo",
                    "Arquivado"
                ]
            )

            observacoes = st.text_area(
                "Observações"
            )

            enviar = st.form_submit_button(
                "Cadastrar projeto"
            )

            if enviar:

                if not titulo:
                    st.error(
                        "Informe o título do projeto."
                    )

                else:

                    inserir(
                        "projetos",
                        [
                            "titulo",
                            "problema",
                            "hipotese",
                            "objetivo",
                            "palavras_chave",
                            "status",
                            "observacoes"
                        ],
                        [
                            titulo,
                            problema,
                            hipotese,
                            objetivo,
                            palavras_chave,
                            status,
                            observacoes
                        ]
                    )

                    st.success(
                        "Projeto cadastrado."
                    )

    with aba2:

        dados, _ = buscar("projetos")

        if not dados:
            st.info(
                "Nenhum projeto cadastrado."
            )

        for projeto in dados:

            (
                id_projeto,
                titulo,
                problema,
                hipotese,
                objetivo,
                palavras_chave,
                status,
                observacoes
            ) = projeto

            with st.expander(titulo):

                st.write(
                    f"**Status:** {status}"
                )

                st.write(
                    f"**Problema:** {problema}"
                )

                st.write(
                    f"**Hipótese:** {hipotese}"
                )

                st.write(
                    f"**Objetivo:** {objetivo}"
                )

                st.write(
                    f"**Palavras-chave:** {palavras_chave}"
                )

                if observacoes:
                    st.write(
                        f"**Observações:** {observacoes}"
                    )

                if st.button(
                    "Excluir projeto",
                    key=f"excluir_projeto_{id_projeto}"
                ):

                    excluir(
                        "projetos",
                        id_projeto
                    )

                    st.rerun()


# ============================================================
# PERIÓDICOS
# ============================================================

elif pagina == "Periódicos":

    st.title("📖 Revistas e periódicos")

    aba1, aba2 = st.tabs(
        ["Cadastrar periódico", "Periódicos cadastrados"]
    )

    with aba1:

        with st.form("form_periodico"):

            nome = st.text_input(
                "Nome da revista"
            )

            issn = st.text_input(
                "ISSN"
            )

            qualis = st.selectbox(
                "Qualis",
                [
                    "Não informado",
                    "A1",
                    "A2",
                    "A3",
                    "A4",
                    "B1",
                    "B2",
                    "B3",
                    "B4",
                    "C"
                ]
            )

            area = st.text_input(
                "Área"
            )

            scopus = st.selectbox(
                "Scopus",
                ["Não informado", "Sim", "Não"]
            )

            web_of_science = st.selectbox(
                "Web of Science",
                ["Não informado", "Sim", "Não"]
            )

            scielo = st.selectbox(
                "SciELO",
                ["Não informado", "Sim", "Não"]
            )

            site = st.text_input(
                "Site"
            )

            observacoes = st.text_area(
                "Observações"
            )

            enviar = st.form_submit_button(
                "Cadastrar periódico"
            )

            if enviar:

                if not nome:
                    st.error(
                        "Informe o nome da revista."
                    )

                else:

                    inserir(
                        "periodicos",
                        [
                            "nome",
                            "issn",
                            "qualis",
                            "area",
                            "scopus",
                            "web_of_science",
                            "scielo",
                            "site",
                            "observacoes"
                        ],
                        [
                            nome,
                            issn,
                            qualis,
                            area,
                            scopus,
                            web_of_science,
                            scielo,
                            site,
                            observacoes
                        ]
                    )

                    st.success(
                        "Periódico cadastrado."
                    )

    with aba2:

        dados, _ = buscar("periodicos")

        if not dados:
            st.info(
                "Nenhum periódico cadastrado."
            )

        for revista in dados:

            (
                id_revista,
                nome,
                issn,
                qualis,
                area,
                scopus,
                web_of_science,
                scielo,
                site,
                observacoes
            ) = revista

            with st.expander(nome):

                st.write(f"**ISSN:** {issn}")
                st.write(f"**Qualis:** {qualis}")
                st.write(f"**Área:** {area}")
                st.write(f"**Scopus:** {scopus}")
                st.write(
                    f"**Web of Science:** {web_of_science}"
                )
                st.write(f"**SciELO:** {scielo}")

                if site:
                    st.write(
                        f"**Site:** {site}"
                    )

                if observacoes:
                    st.write(
                        f"**Observações:** {observacoes}"
                    )

                if st.button(
                    "Excluir periódico",
                    key=f"excluir_periodico_{id_revista}"
                ):

                    excluir(
                        "periodicos",
                        id_revista
                    )

                    st.rerun()


# ============================================================
# SUBMISSÕES
# ============================================================

elif pagina == "Submissões":

    st.title("📤 Submissões")

    artigos, _ = buscar("artigos")
    periodicos, _ = buscar("periodicos")

    nomes_artigos = [
        artigo[1]
        for artigo in artigos
    ]

    nomes_periodicos = [
        revista[1]
        for revista in periodicos
    ]

    if not nomes_artigos:
        st.warning(
            "Cadastre pelo menos um artigo antes de criar uma submissão."
        )

    elif not nomes_periodicos:
        st.warning(
            "Cadastre pelo menos um periódico antes de criar uma submissão."
        )

    else:

        with st.form("form_submissao"):

            artigo = st.selectbox(
                "Artigo",
                nomes_artigos
            )

            periodico = st.selectbox(
                "Periódico",
                nomes_periodicos
            )

            data_submissao = st.date_input(
                "Data da submissão",
                value=date.today()
            )

            status = st.selectbox(
                "Status",
                [
                    "A preparar",
                    "Submetido",
                    "Em avaliação",
                    "Revisões solicitadas",
                    "Aceito",
                    "Rejeitado",
                    "Publicado"
                ]
            )

            prazo = st.text_input(
                "Prazo estimado de avaliação"
            )

            observacoes = st.text_area(
                "Observações"
            )

            enviar = st.form_submit_button(
                "Registrar submissão"
            )

            if enviar:

                inserir(
                    "submissoes",
                    [
                        "artigo",
                        "periodico",
                        "data_submissao",
                        "status",
                        "prazo",
                        "observacoes"
                    ],
                    [
                        artigo,
                        periodico,
                        str(data_submissao),
                        status,
                        prazo,
                        observacoes
                    ]
                )

                st.success(
                    "Submissão registrada."
                )

        st.divider()

        st.subheader(
            "Submissões cadastradas"
        )

        dados, _ = buscar("submissoes")

        for submissao in dados:

            (
                id_submissao,
                artigo,
                periodico,
                data_submissao,
                status,
                prazo,
                observacoes
            ) = submissao

            with st.expander(
                f"{artigo} → {periodico}"
            ):

                st.write(
                    f"**Data:** {data_submissao}"
                )

                st.write(
                    f"**Status:** {status}"
                )

                st.write(
                    f"**Prazo:** {prazo}"
                )

                if observacoes:
                    st.write(
                        f"**Observações:** {observacoes}"
                    )

                if st.button(
                    "Excluir submissão",
                    key=f"excluir_submissao_{id_submissao}"
                ):

                    excluir(
                        "submissoes",
                        id_submissao
                    )

                    st.rerun()


# ============================================================
# PUBLICAÇÕES
# ============================================================

elif pagina == "Publicações":

    st.title("🏆 Publicações")

    with st.form("form_publicacao"):

        artigo = st.text_input(
            "Título do artigo"
        )

        periodico = st.text_input(
            "Revista / periódico"
        )

        doi = st.text_input(
            "DOI"
        )

        data_publicacao = st.date_input(
            "Data de publicação",
            value=date.today()
        )

        link = st.text_input(
            "Link"
        )

        observacoes = st.text_area(
            "Observações"
        )

        enviar = st.form_submit_button(
            "Cadastrar publicação"
        )

        if enviar:

            if not artigo:
                st.error(
                    "Informe o título do artigo."
                )

            else:

                inserir(
                    "publicacoes",
                    [
                        "artigo",
                        "periodico",
                        "doi",
                        "data_publicacao",
                        "link",
                        "observacoes"
                    ],
                    [
                        artigo,
                        periodico,
                        doi,
                        str(data_publicacao),
                        link,
                        observacoes
                    ]
                )

                st.success(
                    "Publicação cadastrada."
                )

    st.divider()

    dados, _ = buscar("publicacoes")

    if not dados:

        st.info(
            "Nenhuma publicação cadastrada."
        )

    for publicacao in dados:

        (
            id_publicacao,
            artigo,
            periodico,
            doi,
            data_publicacao,
            link,
            observacoes
        ) = publicacao

        with st.expander(artigo):

            st.write(
                f"**Periódico:** {periodico}"
            )

            st.write(
                f"**DOI:** {doi}"
            )

            st.write(
                f"**Data:** {data_publicacao}"
            )

            if link:
                st.write(
                    f"**Link:** {link}"
                )

            if observacoes:
                st.write(
                    f"**Observações:** {observacoes}"
                )

            if st.button(
                "Excluir publicação",
                key=f"excluir_publicacao_{id_publicacao}"
            ):

                excluir(
                    "publicacoes",
                    id_publicacao
                )

                st.rerun()
