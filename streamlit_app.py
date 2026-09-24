import streamlit as st
import sqlite3
from datetime import date

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Produção Acadêmica",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB = "producao_academica.db"


# ============================================================
# BANCO DE DADOS
# ============================================================

def conectar():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def criar_banco():
    conn = conectar()
    cursor = conn.cursor()

    # Artigos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artigos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_projeto TEXT NOT NULL,
            titulo TEXT NOT NULL,
            problema TEXT,
            hipotese TEXT,
            objetivo_geral TEXT,
            objetivos_especificos TEXT,
            metodologia TEXT,
            autores TEXT,
            orientador TEXT,
            area TEXT,
            resumo TEXT,
            abstract TEXT,
            palavras_chave TEXT,
            introducao TEXT,
            conclusao TEXT,
            referencias TEXT,
            observacoes TEXT,
            progresso INTEGER DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'desenvolvimento',
            data_criacao TEXT,
            data_atualizacao TEXT
        )
    """)

    # Capítulos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS capitulos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artigo_id INTEGER NOT NULL,
            numero INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            conteudo TEXT,
            FOREIGN KEY (artigo_id) REFERENCES artigos(id)
        )
    """)

    # Periódicos
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

    # Submissões
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artigo_id INTEGER NOT NULL,
            periodico_id INTEGER NOT NULL,
            data_submissao TEXT,
            status TEXT,
            observacoes TEXT,
            FOREIGN KEY (artigo_id) REFERENCES artigos(id),
            FOREIGN KEY (periodico_id) REFERENCES periodicos(id)
        )
    """)

    # Publicações
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS publicacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artigo_id INTEGER NOT NULL,
            periodico_id INTEGER,
            doi TEXT,
            data_publicacao TEXT,
            link TEXT,
            observacoes TEXT,
            FOREIGN KEY (artigo_id) REFERENCES artigos(id),
            FOREIGN KEY (periodico_id) REFERENCES periodicos(id)
        )
    """)

    conn.commit()
    conn.close()


criar_banco()


# ============================================================
# FUNÇÕES DO BANCO
# ============================================================

def executar(sql, parametros=()):
    conn = conectar()
    conn.execute(sql, parametros)
    conn.commit()
    conn.close()


def consultar(sql, parametros=()):
    conn = conectar()
    resultado = conn.execute(sql, parametros).fetchall()
    conn.close()
    return resultado


def buscar_artigo(artigo_id):
    resultado = consultar(
        "SELECT * FROM artigos WHERE id = ?",
        (artigo_id,)
    )

    if resultado:
        return resultado[0]

    return None


def buscar_capitulos(artigo_id):
    return consultar(
        """
        SELECT *
        FROM capitulos
        WHERE artigo_id = ?
        ORDER BY numero
        """,
        (artigo_id,)
    )


def contar_artigos(status):
    resultado = consultar(
        """
        SELECT COUNT(*) AS total
        FROM artigos
        WHERE status = ?
        """,
        (status,)
    )

    return resultado[0]["total"]


# ============================================================
# ESTILO
# ============================================================

st.markdown("""
<style>

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    .titulo {
        font-size: 2.2rem;
        font-weight: 700;
        color: #172033;
        margin-bottom: 0.2rem;
    }

    .subtitulo {
        color: #6b7280;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    .card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }

    .card-title {
        font-size: 1.05rem;
        font-weight: 650;
        color: #172033;
    }

    .card-description {
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: 0.35rem;
    }

    .metric {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 1.2rem;
    }

    .metric-label {
        color: #6b7280;
        font-size: 0.85rem;
    }

    .metric-value {
        color: #172033;
        font-size: 2rem;
        font-weight: 700;
        margin-top: 0.25rem;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# MENU
# ============================================================

st.sidebar.markdown(
    """
    <div style="
        font-size: 1.45rem;
        font-weight: 700;
        color: #172033;
        margin-bottom: 1.5rem;
    ">
        📚 Produção Acadêmica
    </div>
    """,
    unsafe_allow_html=True
)

pagina = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Artigos em Projeto",
        "Artigos em Desenvolvimento",
        "Concluídos para Submissão",
        "Periódicos",
        "Submissões",
        "Publicações"
    ]
)

st.sidebar.divider()

st.sidebar.caption("Sistema de produção científica")


# ============================================================
# DASHBOARD
# ============================================================

if pagina == "Dashboard":

    st.markdown(
        '<div class="titulo">Produção Acadêmica</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitulo">Acompanhe sua produção científica.</div>',
        unsafe_allow_html=True
    )

    projeto = contar_artigos("projeto")
    desenvolvimento = contar_artigos("desenvolvimento")
    concluido = contar_artigos("concluido")
    submetido = contar_artigos("submetido")
    publicado = contar_artigos("publicado")

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.markdown(
            f"""
            <div class="metric">
                <div class="metric-label">Projetos</div>
                <div class="metric-value">{projeto}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric">
                <div class="metric-label">Desenvolvimento</div>
                <div class="metric-value">{desenvolvimento}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric">
                <div class="metric-label">Prontos</div>
                <div class="metric-value">{concluido}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="metric">
                <div class="metric-label">Submetidos</div>
                <div class="metric-value">{submetido}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c5:
        st.markdown(
            f"""
            <div class="metric">
                <div class="metric-label">Publicados</div>
                <div class="metric-value">{publicado}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")
    st.divider()

    st.subheader("Fluxo da produção")

    fluxo = st.columns(4)

    with fluxo[0]:
        st.markdown("### 01")
        st.write("Projeto")
        st.metric("Artigos", projeto)

    with fluxo[1]:
        st.markdown("### 02")
        st.write("Desenvolvimento")
        st.metric("Artigos", desenvolvimento)

    with fluxo[2]:
        st.markdown("### 03")
        st.write("Prontos para submissão")
        st.metric("Artigos", concluido)

    with fluxo[3]:
        st.markdown("### 04")
        st.write("Publicados")
        st.metric("Artigos", publicado)

    st.divider()

    st.subheader("Artigos em desenvolvimento")

    artigos = consultar("""
        SELECT id, nome_projeto, titulo, progresso
        FROM artigos
        WHERE status = 'desenvolvimento'
        ORDER BY data_atualizacao DESC
    """)

    if not artigos:
        st.info("Nenhum artigo em desenvolvimento.")

    for artigo in artigos:

        titulo = artigo["titulo"] or artigo["nome_projeto"]
        progresso = artigo["progresso"] or 0

        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">{titulo}</div>
                <div class="card-description">
                    {artigo["nome_projeto"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(progresso / 100)

        st.caption(f"{progresso}% concluído")


# ============================================================
# ARTIGOS EM PROJETO
# ============================================================

elif pagina == "Artigos em Projeto":

    st.markdown(
        '<div class="titulo">Artigos em Projeto</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitulo">Crie a estrutura inicial de um novo artigo.</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Ao criar um projeto, ele será automaticamente encaminhado para "
        "Artigos em Desenvolvimento."
    )

    with st.form("novo_artigo"):

        st.subheader("Identificação")

        col1, col2 = st.columns(2)

        with col1:

            nome_projeto = st.text_input(
                "Nome do projeto"
            )

        with col2:

            titulo = st.text_input(
                "Título provisório"
            )

        autores = st.text_input(
            "Autores"
        )

        col1, col2 = st.columns(2)

        with col1:

            orientador = st.text_input(
                "Orientador"
            )

        with col2:

            area = st.text_input(
                "Área / linha de pesquisa"
            )

        st.divider()

        st.subheader("Projeto de pesquisa")

        problema = st.text_area(
            "Problema de pesquisa",
            height=130
        )

        hipotese = st.text_area(
            "Hipótese",
            height=130
        )

        objetivo_geral = st.text_area(
            "Objetivo geral",
            height=130
        )

        objetivos_especificos = st.text_area(
            "Objetivos específicos",
            height=150
        )

        metodologia = st.text_area(
            "Metodologia",
            height=150
        )

        palavras_chave = st.text_input(
            "Palavras-chave"
        )

        observacoes = st.text_area(
            "Observações"
        )

        criar = st.form_submit_button(
            "Criar projeto",
            use_container_width=True
        )

        if criar:

            if not nome_projeto.strip():
                st.error("Informe o nome do projeto.")

            elif not titulo.strip():
                st.error("Informe o título provisório.")

            else:

                hoje = str(date.today())

                conn = conectar()

                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO artigos (
                        nome_projeto,
                        titulo,
                        problema,
                        hipotese,
                        objetivo_geral,
                        objetivos_especificos,
                        metodologia,
                        autores,
                        orientador,
                        area,
                        palavras_chave,
                        observacoes,
                        progresso,
                        status,
                        data_criacao,
                        data_atualizacao
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        nome_projeto.strip(),
                        titulo.strip(),
                        problema,
                        hipotese,
                        objetivo_geral,
                        objetivos_especificos,
                        metodologia,
                        autores,
                        orientador,
                        area,
                        palavras_chave,
                        observacoes,
                        0,
                        "desenvolvimento",
                        hoje,
                        hoje
                    )
                )

                conn.commit()
                conn.close()

                st.success(
                    "Projeto criado com sucesso."
                )

                st.info(
                    "O artigo foi automaticamente encaminhado para "
                    "'Artigos em Desenvolvimento'."
                )


# ============================================================
# ARTIGOS EM DESENVOLVIMENTO
# ============================================================

elif pagina == "Artigos em Desenvolvimento":

    st.markdown(
        '<div class="titulo">Artigos em Desenvolvimento</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitulo">Desenvolva o texto completo do artigo.</div>',
        unsafe_allow_html=True
    )

    artigos = consultar("""
        SELECT *
        FROM artigos
        WHERE status = 'desenvolvimento'
        ORDER BY data_atualizacao DESC
    """)

    if not artigos:

        st.info(
            "Você ainda não possui artigos em desenvolvimento."
        )

    for artigo in artigos:

        titulo = artigo["titulo"]

        with st.expander(
            f"📄 {titulo}"
        ):

            st.caption(
                f"Projeto: {artigo['nome_projeto']}"
            )

            st.divider()

            st.subheader("Informações principais")

            novo_titulo = st.text_input(
                "Título",
                value=artigo["titulo"],
                key=f"titulo_{artigo['id']}"
            )

            resumo = st.text_area(
                "Resumo",
                value=artigo["resumo"] or "",
                height=180,
                key=f"resumo_{artigo['id']}"
            )

            abstract = st.text_area(
                "Abstract",
                value=artigo["abstract"] or "",
                height=180,
                key=f"abstract_{artigo['id']}"
            )

            palavras = st.text_input(
                "Palavras-chave",
                value=artigo["palavras_chave"] or "",
                key=f"palavras_{artigo['id']}"
            )

            st.divider()

            st.subheader("Texto do artigo")

            introducao = st.text_area(
                "Introdução",
                value=artigo["introducao"] or "",
                height=250,
                key=f"introducao_{artigo['id']}"
            )

            st.divider()

            st.subheader("Capítulos")

            capitulos = buscar_capitulos(
                artigo["id"]
            )

            for capitulo in capitulos:

                with st.container(border=True):

                    st.markdown(
                        f"### Capítulo {capitulo['numero']}"
                    )

                    novo_titulo_capitulo = st.text_input(
                        "Título do capítulo",
                        value=capitulo["titulo"],
                        key=f"capitulo_titulo_{capitulo['id']}"
                    )

                    novo_conteudo = st.text_area(
                        "Conteúdo",
                        value=capitulo["conteudo"] or "",
                        height=300,
                        key=f"capitulo_conteudo_{capitulo['id']}"
                    )

                    col1, col2 = st.columns([5, 1])

                    with col1:

                        if st.button(
                            "Salvar capítulo",
                            key=f"salvar_capitulo_{capitulo['id']}"
                        ):

                            executar(
                                """
                                UPDATE capitulos
                                SET titulo = ?, conteudo = ?
                                WHERE id = ?
                                """,
                                (
                                    novo_titulo_capitulo,
                                    novo_conteudo,
                                    capitulo["id"]
                                )
                            )

                            st.success(
                                "Capítulo salvo."
                            )

                            st.rerun()

                    with col2:

                        if st.button(
                            "Excluir",
                            key=f"excluir_capitulo_{capitulo['id']}"
                        ):

                            executar(
                                """
                                DELETE FROM capitulos
                                WHERE id = ?
                                """,
                                (capitulo["id"],)
                            )

                            st.rerun()

            if st.button(
                "＋ Adicionar capítulo",
                key=f"novo_capitulo_{artigo['id']}"
            ):

                ultimo = consultar(
                    """
                    SELECT MAX(numero) AS maior
                    FROM capitulos
                    WHERE artigo_id = ?
                    """,
                    (artigo["id"],)
                )

                maior = ultimo[0]["maior"]

                if maior is None:
                    numero = 1
                else:
                    numero = maior + 1

                executar(
                    """
                    INSERT INTO capitulos (
                        artigo_id,
                        numero,
                        titulo,
                        conteudo
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        artigo["id"],
                        numero,
                        f"Capítulo {numero}",
                        ""
                    )
                )

                st.rerun()

            st.divider()

            conclusao = st.text_area(
                "Conclusão",
                value=artigo["conclusao"] or "",
                height=250,
                key=f"conclusao_{artigo['id']}"
            )

            referencias = st.text_area(
                "Referências",
                value=artigo["referencias"] or "",
                height=300,
                key=f"referencias_{artigo['id']}"
            )

            observacoes = st.text_area(
                "Observações",
                value=artigo["observacoes"] or "",
                height=120,
                key=f"observacoes_{artigo['id']}"
            )

            progresso = st.slider(
                "Progresso do artigo",
                min_value=0,
                max_value=100,
                value=int(artigo["progresso"] or 0),
                key=f"progresso_{artigo['id']}"
            )

            st.divider()

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "💾 Salvar artigo",
                    key=f"salvar_artigo_{artigo['id']}",
                    use_container_width=True
                ):

                    executar(
                        """
                        UPDATE artigos
                        SET
                            titulo = ?,
                            resumo = ?,
                            abstract = ?,
                            palavras_chave = ?,
                            introducao = ?,
                            conclusao = ?,
                            referencias = ?,
                            observacoes = ?,
                            progresso = ?,
                            data_atualizacao = ?
                        WHERE id = ?
                        """,
                        (
                            novo_titulo,
                            resumo,
                            abstract,
                            palavras,
                            introducao,
                            conclusao,
                            referencias,
                            observacoes,
                            progresso,
                            str(date.today()),
                            artigo["id"]
                        )
                    )

                    st.success(
                        "Artigo salvo com sucesso."
                    )

                    st.rerun()

            with col2:

                if st.button(
                    "✓ Concluir para submissão",
                    key=f"concluir_{artigo['id']}",
                    use_container_width=True
                ):

                    executar(
                        """
                        UPDATE artigos
                        SET
                            status = 'concluido',
                            progresso = 100,
                            data_atualizacao = ?
                        WHERE id = ?
                        """,
                        (
                            str(date.today()),
                            artigo["id"]
                        )
                    )

                    st.success(
                        "Artigo enviado para 'Concluídos para Submissão'."
                    )

                    st.rerun()


# ============================================================
# CONCLUÍDOS PARA SUBMISSÃO
# ============================================================

elif pagina == "Concluídos para Submissão":

    st.markdown(
        '<div class="titulo">Concluídos para Submissão</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitulo">Artigos finalizados e prontos para escolha do periódico.</div>',
        unsafe_allow_html=True
    )

    artigos = consultar("""
        SELECT *
        FROM artigos
        WHERE status = 'concluido'
        ORDER BY data_atualizacao DESC
    """)

    if not artigos:

        st.info(
            "Nenhum artigo concluído para submissão."
        )

    for artigo in artigos:

        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">
                    {artigo["titulo"]}
                </div>

                <div class="card-description">
                    Projeto: {artigo["nome_projeto"]}
                </div>

                <div class="card-description">
                    Autores: {artigo["autores"] or "Não informado"}
                </div>

                <div class="card-description">
                    Área: {artigo["area"] or "Não informada"}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.expander("Ver artigo"):

            st.write(
                "**Resumo**"
            )

            st.write(
                artigo["resumo"] or "Não informado."
            )

            st.write(
                "**Palavras-chave**"
            )

            st.write(
                artigo["palavras_chave"] or "Não informado."
            )

            st.write(
                "**Conclusão**"
            )

            st.write(
                artigo["conclusao"] or "Não informada."
            )

            st.write(
                "**Referências**"
            )

            st.write(
                artigo["referencias"] or "Não informadas."
            )

            st.divider()

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "↩ Voltar para desenvolvimento",
                    key=f"voltar_{artigo['id']}",
                    use_container_width=True
                ):

                    executar(
                        """
                        UPDATE artigos
                        SET
                            status = 'desenvolvimento',
                            data_atualizacao = ?
                        WHERE id = ?
                        """,
                        (
                            str(date.today()),
                            artigo["id"]
                        )
                    )

                    st.rerun()

            with col2:

                if st.button(
                    "Excluir artigo",
                    key=f"excluir_{artigo['id']}",
                    use_container_width=True
                ):

                    executar(
                        """
                        DELETE FROM capitulos
                        WHERE artigo_id = ?
                        """,
                        (artigo["id"],)
                    )

                    executar(
                        """
                        DELETE FROM artigos
                        WHERE id = ?
                        """,
                        (artigo["id"],)
                    )

                    st.rerun()


# ============================================================
# PERIÓDICOS
# ============================================================

elif pagina == "Periódicos":

    st.markdown(
        '<div class="titulo">Periódicos</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitulo">Cadastre as revistas para as quais seus artigos podem ser submetidos.</div>',
        unsafe_allow_html=True
    )

    with st.expander(
        "＋ Cadastrar periódico",
        expanded=True
    ):

        with st.form("novo_periodico"):

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

            col1, col2, col3 = st.columns(3)

            with col1:

                scopus = st.selectbox(
                    "Scopus",
                    ["Não informado", "Sim", "Não"]
                )

            with col2:

                wos = st.selectbox(
                    "Web of Science",
                    ["Não informado", "Sim", "Não"]
                )

            with col3:

                scielo = st.selectbox(
                    "SciELO",
                    ["Não informado", "Sim", "Não"]
                )

            site = st.text_input(
                "Site da revista"
            )

            observacoes = st.text_area(
                "Observações"
            )

            salvar = st.form_submit_button(
                "Cadastrar periódico",
                use_container_width=True
            )

            if salvar:

                if not nome.strip():

                    st.error(
                        "Informe o nome da revista."
                    )

                else:

                    executar(
                        """
                        INSERT INTO periodicos (
                            nome,
                            issn,
                            qualis,
                            area,
                            scopus,
                            web_of_science,
                            scielo,
                            site,
                            observacoes
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            nome,
                            issn,
                            qualis,
                            area,
                            scopus,
                            wos,
                            scielo,
                            site,
                            observacoes
                        )
                    )

                    st.success(
                        "Periódico cadastrado."
                    )

                    st.rerun()

    st.divider()

    periodicos = consultar(
        "SELECT * FROM periodicos ORDER BY nome"
    )

    if not periodicos:

        st.info(
            "Nenhum periódico cadastrado."
        )

    for periodico in periodicos:

        with st.container(border=True):

            col1, col2 = st.columns([5, 1])

            with col1:

                st.subheader(
                    periodico["nome"]
                )

                st.caption(
                    f"ISSN: {periodico['issn'] or 'Não informado'}"
                )

                st.caption(
                    f"Qualis: {periodico['qualis']}"
                )

                st.caption(
                    f"Área: {periodico['area'] or 'Não informada'}"
                )

            with col2:

                if st.button(
                    "Excluir",
                    key=f"excluir_periodico_{periodico['id']}"
                ):

                    executar(
                        """
                        DELETE FROM periodicos
                        WHERE id = ?
                        """,
                        (periodico["id"],)
                    )

                    st.rerun()


# ============================================================
# SUBMISSÕES
# ============================================================

elif pagina == "Submissões":

    st.markdown(
        '<div class="titulo">Submissões</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitulo">Controle dos artigos enviados aos periódicos.</div>',
        unsafe_allow_html=True
    )

    artigos = consultar("""
        SELECT id, titulo
        FROM artigos
        WHERE status IN ('concluido', 'submetido')
        ORDER BY titulo
    """)

    periodicos = consultar("""
        SELECT id, nome
        FROM periodicos
        ORDER BY nome
    """)

    if not artigos:

        st.warning(
            "Você precisa ter um artigo concluído para criar uma submissão."
        )

    elif not periodicos:

        st.warning(
            "Cadastre pelo menos um periódico."
        )

    else:

        with st.form("nova_submissao"):

            artigo_escolhido = st.selectbox(
                "Artigo",
                artigos,
                format_func=lambda x: x["titulo"]
            )

            periodico_escolhido = st.selectbox(
                "Periódico",
                periodicos,
                format_func=lambda x: x["nome"]
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
                    "Rejeitado"
                ]
            )

            observacoes = st.text_area(
                "Observações"
            )

            salvar = st.form_submit_button(
                "Registrar submissão",
                use_container_width=True
            )

            if salvar:

                executar(
                    """
                    INSERT INTO submissoes (
                        artigo_id,
                        periodico_id,
                        data_submissao,
                        status,
                        observacoes
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        artigo_escolhido["id"],
                        periodico_escolhido["id"],
                        str(data_submissao),
                        status,
                        observacoes
                    )
                )

                executar(
                    """
                    UPDATE artigos
                    SET status = 'submetido',
                        data_atualizacao = ?
                    WHERE id = ?
                    """,
                    (
                        str(date.today()),
                        artigo_escolhido["id"]
                    )
                )

                st.success(
                    "Submissão registrada."
                )

                st.rerun()

    st.divider()

    submissoes = consultar("""
        SELECT
            s.id,
            a.titulo AS artigo,
            p.nome AS periodico,
            s.data_submissao,
            s.status,
            s.observacoes
        FROM submissoes s
        JOIN artigos a ON a.id = s.artigo_id
        JOIN periodicos p ON p.id = s.periodico_id
        ORDER BY s.id DESC
    """)

    if not submissoes:

        st.info(
            "Nenhuma submissão registrada."
        )

    for submissao in submissoes:

        with st.container(border=True):

            st.subheader(
                submissao["artigo"]
            )

            st.write(
                f"**Periódico:** {submissao['periodico']}"
            )

            st.write(
                f"**Data:** {submissao['data_submissao']}"
            )

            st.write(
                f"**Status:** {submissao['status']}"
            )

            if submissao["observacoes"]:

                st.caption(
                    submissao["observacoes"]
                )


# ============================================================
# PUBLICAÇÕES
# ============================================================

elif pagina == "Publicações":

    st.markdown(
        '<div class="titulo">Publicações</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitulo">Registre os artigos publicados.</div>',
        unsafe_allow_html=True
    )

    artigos = consultar("""
        SELECT id, titulo
        FROM artigos
        WHERE status = 'submetido'
        ORDER BY titulo
    """)

    periodicos = consultar("""
        SELECT id, nome
        FROM periodicos
        ORDER BY nome
    """)

    if artigos:

        with st.form("nova_publicacao"):

            artigo_escolhido = st.selectbox(
                "Artigo",
                artigos,
                format_func=lambda x: x["titulo"]
            )

            periodico_escolhido = st.selectbox(
                "Periódico",
                periodicos,
                format_func=lambda x: x["nome"]
            ) if periodicos else None

            doi = st.text_input(
                "DOI"
            )

            data_publicacao = st.date_input(
                "Data de publicação",
                value=date.today()
            )

            link = st.text_input(
                "Link da publicação"
            )

            observacoes = st.text_area(
                "Observações"
            )

            salvar = st.form_submit_button(
                "Registrar publicação",
                use_container_width=True
            )

            if salvar:

                periodico_id = (
                    periodico_escolhido["id"]
                    if periodico_escolhido
                    else None
                )

                executar(
                    """
                    INSERT INTO publicacoes (
                        artigo_id,
                        periodico_id,
                        doi,
                        data_publicacao,
                        link,
                        observacoes
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        artigo_escolhido["id"],
                        periodico_id,
                        doi,
                        str(data_publicacao),
                        link,
                        observacoes
                    )
                )

                executar(
                    """
                    UPDATE artigos
                    SET status = 'publicado',
                        data_atualizacao = ?
                    WHERE id = ?
                    """,
                    (
                        str(date.today()),
                        artigo_escolhido["id"]
                    )
                )

                st.success(
                    "Publicação registrada."
                )

                st.rerun()

    else:

        st.info(
            "Não há artigos submetidos para registrar como publicados."
        )

    st.divider()

    publicacoes = consultar("""
        SELECT
            pu.id,
            a.titulo AS artigo,
            p.nome AS periodico,
            pu.doi,
            pu.data_publicacao,
            pu.link
        FROM publicacoes pu
        JOIN artigos a ON a.id = pu.artigo_id
        LEFT JOIN periodicos p ON p.id = pu.periodico_id
        ORDER BY pu.data_publicacao DESC
    """)

    for publicacao in publicacoes:

        with st.container(border=True):

            st.subheader(
                publicacao["artigo"]
            )

            st.write(
                f"**Periódico:** "
                f"{publicacao['periodico'] or 'Não informado'}"
            )

            st.write(
                f"**DOI:** "
                f"{publicacao['doi'] or 'Não informado'}"
            )

            st.write(
                f"**Data:** "
                f"{publicacao['data_publicacao']}"
            )

            if publicacao["link"]:

                st.write(
                    f"**Link:** {publicacao['link']}"
                )
