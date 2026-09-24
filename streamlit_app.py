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

DB = "academia.db"


# ============================================================
# ESTILO
# ============================================================

st.markdown("""
<style>

    .main {
        background-color: #f7f8fa;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }

    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e8e8e8;
    }

    .titulo-principal {
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
        background: white;
        padding: 1.3rem;
        border-radius: 14px;
        border: 1px solid #e8e8e8;
        margin-bottom: 1rem;
    }

    .card-titulo {
        font-size: 1.1rem;
        font-weight: 650;
        color: #172033;
        margin-bottom: 0.4rem;
    }

    .card-meta {
        color: #6b7280;
        font-size: 0.9rem;
    }

    .status {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        background: #eef2ff;
        color: #4338ca;
    }

    .metric-card {
        background: white;
        border: 1px solid #e8e8e8;
        border-radius: 14px;
        padding: 1.2rem;
    }

    .metric-label {
        color: #6b7280;
        font-size: 0.85rem;
    }

    .metric-number {
        color: #172033;
        font-size: 2rem;
        font-weight: 700;
        margin-top: 0.2rem;
    }

    div[data-testid="stForm"] {
        background: white;
        padding: 1.5rem;
        border-radius: 14px;
        border: 1px solid #e8e8e8;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# BANCO
# ============================================================

def conectar():
    return sqlite3.connect(DB)


def criar_banco():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artigos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nome_projeto TEXT,
            titulo TEXT,

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

            capitulo_1_titulo TEXT,
            capitulo_1 TEXT,

            capitulo_2_titulo TEXT,
            capitulo_2 TEXT,

            capitulo_3_titulo TEXT,
            capitulo_3 TEXT,

            capitulo_4_titulo TEXT,
            capitulo_4 TEXT,

            conclusao TEXT,
            referencias TEXT,

            observacoes TEXT,

            progresso INTEGER DEFAULT 0,

            status TEXT DEFAULT 'desenvolvimento',

            data_criacao TEXT,
            data_atualizacao TEXT
        )
    """)

    conn.commit()
    conn.close()


criar_banco()


# ============================================================
# FUNÇÕES
# ============================================================

def executar(sql, parametros=()):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(sql, parametros)

    conn.commit()
    conn.close()


def buscar(sql, parametros=()):

    conn = conectar()

    dados = conn.execute(
        sql,
        parametros
    ).fetchall()

    conn.close()

    return dados


def buscar_artigo(id_artigo):

    dados = buscar(
        "SELECT * FROM artigos WHERE id = ?",
        (id_artigo,)
    )

    if dados:
        return dados[0]

    return None


def contar(status):

    resultado = buscar(
        "SELECT COUNT(*) FROM artigos WHERE status = ?",
        (status,)
    )

    return resultado[0][0]


# ============================================================
# MENU
# ============================================================

st.sidebar.markdown(
    """
    <div style="
        font-size: 1.4rem;
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
    "Navegação",
    [
        "Dashboard",
        "Artigos em Projeto",
        "Artigos em Desenvolvimento",
        "Concluídos para submissão"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "Sistema pessoal de produção científica"
)


# ============================================================
# DASHBOARD
# ============================================================

if pagina == "Dashboard":

    st.markdown(
        '<div class="titulo-principal">Produção Acadêmica</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitulo">Visão geral da sua produção científica</div>',
        unsafe_allow_html=True
    )

    projetos = contar("projeto")
    desenvolvimento = contar("desenvolvimento")
    concluidos = contar("concluido")
    submetidos = contar("submetido")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Em projeto</div>
                <div class="metric-number">{projetos}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Em desenvolvimento</div>
                <div class="metric-number">{desenvolvimento}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Prontos para submissão</div>
                <div class="metric-number">{concluidos}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Submetidos</div>
                <div class="metric-number">{submetidos}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")
    st.divider()

    st.subheader("Fluxo de produção")

    st.write(
        "Acompanhe seus artigos desde a ideia inicial até a submissão."
    )

    fluxo = [
        ("1", "Projeto", projetos),
        ("2", "Desenvolvimento", desenvolvimento),
        ("3", "Concluído", concluidos),
        ("4", "Submetido", submetidos),
    ]

    cols = st.columns(4)

    for col, (numero, nome, quantidade) in zip(cols, fluxo):

        with col:

            st.markdown(
                f"""
                <div class="card">
                    <div style="
                        font-size:0.8rem;
                        color:#6b7280;
                    ">
                        ETAPA {numero}
                    </div>

                    <div class="card-titulo">
                        {nome}
                    </div>

                    <div style="
                        font-size:1.8rem;
                        font-weight:700;
                        color:#172033;
                    ">
                        {quantidade}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    st.subheader("Artigos em desenvolvimento")

    artigos = buscar("""
        SELECT id, titulo, nome_projeto, progresso
        FROM artigos
        WHERE status = 'desenvolvimento'
        ORDER BY data_atualizacao DESC
    """)

    if not artigos:

        st.info("Nenhum artigo em desenvolvimento.")

    else:

        for artigo in artigos:

            id_artigo, titulo, nome_projeto, progresso = artigo

            titulo_exibicao = titulo or nome_projeto or "Sem título"

            st.markdown(
                f"""
                <div class="card">
                    <div class="card-titulo">
                        {titulo_exibicao}
                    </div>

                    <div class="card-meta">
                        {nome_projeto or "Projeto não informado"}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(
                progresso / 100
            )

            st.caption(
                f"{progresso}% concluído"
            )


# ============================================================
# ARTIGOS EM PROJETO
# ============================================================

elif pagina == "Artigos em Projeto":

    st.markdown(
        '<div class="titulo-principal">Novo artigo</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitulo">Cadastre a estrutura inicial do projeto de pesquisa</div>',
        unsafe_allow_html=True
    )

    with st.form("novo_projeto"):

        st.subheader("Identificação")

        c1, c2 = st.columns(2)

        with c1:

            nome_projeto = st.text_input(
                "Nome do projeto"
            )

        with c2:

            titulo = st.text_input(
                "Título provisório"
            )

        autores = st.text_input(
            "Autores"
        )

        c1, c2 = st.columns(2)

        with c1:

            orientador = st.text_input(
                "Orientador"
            )

        with c2:

            area = st.text_input(
                "Área / linha de pesquisa"
            )

        st.divider()

        st.subheader("Projeto de pesquisa")

        problema = st.text_area(
            "Problema de pesquisa",
            height=120
        )

        hipotese = st.text_area(
            "Hipótese",
            height=120
        )

        objetivo_geral = st.text_area(
            "Objetivo geral",
            height=120
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
            "Observações iniciais",
            height=100
        )

        enviar = st.form_submit_button(
            "Criar projeto e iniciar desenvolvimento",
            use_container_width=True
        )

        if enviar:

            if not nome_projeto:

                st.error(
                    "Informe o nome do projeto."
                )

            elif not titulo:

                st.error(
                    "Informe o título provisório."
                )

            else:

                agora = str(date.today())

                executar("""
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
                """, (
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
                    0,
                    "desenvolvimento",
                    agora,
                    agora
                ))

                st.success(
                    "Projeto criado. O artigo já foi encaminhado para Desenvolvimento."
                )

                st.info(
                    "Agora acesse 'Artigos em Desenvolvimento' para continuar a redação."
                )


# ============================================================
# ARTIGOS EM DESENVOLVIMENTO
# ============================================================

elif pagina == "Artigos em Desenvolvimento":

    st.markdown(
        '<div class="titulo-principal">Artigos em Desenvolvimento</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitulo">Área de redação e construção dos artigos</div>',
        unsafe_allow_html=True
    )

    artigos = buscar("""
        SELECT id, nome_projeto, titulo, progresso
        FROM artigos
        WHERE status = 'desenvolvimento'
        ORDER BY data_atualizacao DESC
    """)

    if not artigos:

        st.info(
            "Nenhum artigo em desenvolvimento."
        )

    for artigo in artigos:

        id_artigo, nome_projeto, titulo, progresso = artigo

        nome = titulo or nome_projeto or "Sem título"

        with st.expander(
            f"📄 {nome}"
        ):

            st.caption(
                f"Projeto: {nome_projeto or 'Não informado'}"
            )

            st.divider()

            dados = buscar_artigo(id_artigo)

            # índices correspondentes às colunas da tabela

            st.subheader("Informações do artigo")

            novo_titulo = st.text_input(
                "Título",
                value=dados[2] or "",
                key=f"titulo_{id_artigo}"
            )

            resumo = st.text_area(
                "Resumo",
                value=dados[19] or "",
                height=180,
                key=f"resumo_{id_artigo}"
            )

            abstract = st.text_area(
                "Abstract",
                value=dados[20] or "",
                height=180,
                key=f"abstract_{id_artigo}"
            )

            palavras = st.text_input(
                "Palavras-chave",
                value=dados[21] or "",
                key=f"palavras_{id_artigo}"
            )

            st.divider()

            st.subheader("Estrutura do artigo")

            introducao = st.text_area(
                "Introdução",
                value=dados[22] or "",
                height=220,
                key=f"intro_{id_artigo}"
            )

            c1, c2 = st.columns(2)

            with c1:

                cap1_titulo = st.text_input(
                    "Título do Capítulo 1",
                    value=dados[23] or "",
                    key=f"cap1t_{id_artigo}"
                )

                cap1 = st.text_area(
                    "Conteúdo do Capítulo 1",
                    value=dados[24] or "",
                    height=250,
                    key=f"cap1_{id_artigo}"
                )

            with c2:

                cap2_titulo = st.text_input(
                    "Título do Capítulo 2",
                    value=dados[25] or "",
                    key=f"cap2t_{id_artigo}"
                )

                cap2 = st.text_area(
                    "Conteúdo do Capítulo 2",
                    value=dados[26] or "",
                    height=250,
                    key=f"cap2_{id_artigo}"
                )

            c1, c2 = st.columns(2)

            with c1:

                cap3_titulo = st.text_input(
                    "Título do Capítulo 3",
                    value=dados[27] or "",
                    key=f"cap3t_{id_artigo}"
                )

                cap3 = st.text_area(
                    "Conteúdo do Capítulo 3",
                    value=dados[28] or "",
                    height=250,
                    key=f"cap3_{id_artigo}"
                )

            with c2:

                cap4_titulo = st.text_input(
                    "Título do Capítulo 4",
                    value=dados[29] or "",
                    key=f"cap4t_{id_artigo}"
                )

                cap4 = st.text_area(
                    "Conteúdo do Capítulo 4",
                    value=dados[30] or "",
                    height=250,
                    key=f"cap4_{id_artigo}"
                )

            conclusao = st.text_area(
                "Conclusão",
                value=dados[31] or "",
                height=220,
                key=f"conclusao_{id_artigo}"
            )

            referencias = st.text_area(
                "Referências",
                value=dados[32] or "",
                height=250,
                key=f"referencias_{id_artigo}"
            )

            st.divider()

            progresso_novo = st.slider(
                "Percentual de conclusão",
                0,
                100,
                int(dados[34] or 0),
                key=f"progresso_{id_artigo}"
            )

            observacoes = st.text_area(
                "Observações",
                value=dados[33] or "",
                height=120,
                key=f"obs_{id_artigo}"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "💾 Salvar alterações",
                    key=f"salvar_{id_artigo}",
                    use_container_width=True
                ):

                    executar("""
                        UPDATE artigos
                        SET
                            titulo = ?,
                            resumo = ?,
                            abstract = ?,
                            palavras_chave = ?,
                            introducao = ?,
                            capitulo_1_titulo = ?,
                            capitulo_1 = ?,
                            capitulo_2_titulo = ?,
                            capitulo_2 = ?,
                            capitulo_3_titulo = ?,
                            capitulo_3 = ?,
                            capitulo_4_titulo = ?,
                            capitulo_4 = ?,
                            conclusao = ?,
                            referencias = ?,
                            observacoes = ?,
                            progresso = ?,
                            data_atualizacao = ?
                        WHERE id = ?
                    """, (
                        novo_titulo,
                        resumo,
                        abstract,
                        palavras,
                        introducao,
                        cap1_titulo,
                        cap1,
                        cap2_titulo,
                        cap2,
                        cap3_titulo,
                        cap3,
                        cap4_titulo,
                        cap4,
                        conclusao,
                        referencias,
                        observacoes,
                        progresso_novo,
                        str(date.today()),
                        id_artigo
                    ))

                    st.success(
                        "Alterações salvas."
                    )

                    st.rerun()

            with col2:

                if st.button(
                    "✓ Concluir para submissão",
                    key=f"concluir_{id_artigo}",
                    use_container_width=True
                ):

                    executar("""
                        UPDATE artigos
                        SET
                            status = 'concluido',
                            progresso = 100,
                            data_atualizacao = ?
                        WHERE id = ?
                    """, (
                        str(date.today()),
                        id_artigo
                    ))

                    st.success(
                        "Artigo encaminhado para Concluídos para submissão."
                    )

                    st.rerun()


# ============================================================
# CONCLUÍDOS PARA SUBMISSÃO
# ============================================================

elif pagina == "Concluídos para submissão":

    st.markdown(
        '<div class="titulo-principal">Concluídos para submissão</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitulo">Artigos finalizados e prontos para escolha do periódico</div>',
        unsafe_allow_html=True
    )

    artigos = buscar("""
        SELECT id, nome_projeto, titulo, autores, area
        FROM artigos
        WHERE status = 'concluido'
        ORDER BY data_atualizacao DESC
    """)

    if not artigos:

        st.info(
            "Ainda não há artigos concluídos para submissão."
        )

    for artigo in artigos:

        (
            id_artigo,
            nome_projeto,
            titulo,
            autores,
            area
        ) = artigo

        nome = titulo or nome_projeto or "Sem título"

        st.markdown(
            f"""
            <div class="card">
                <div class="card-titulo">
                    {nome}
                </div>

                <div class="card-meta">
                    Projeto: {nome_projeto or "Não informado"}
                </div>

                <div class="card-meta">
                    Autores: {autores or "Não informado"}
                </div>

                <div class="card-meta">
                    Área: {area or "Não informada"}
                </div>

                <br>

                <span class="status">
                    PRONTO PARA SUBMISSÃO
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        dados = buscar_artigo(id_artigo)

        with st.expander("Abrir artigo"):

            st.write(
                f"**Título:** {dados[2]}"
            )

            st.write(
                f"**Resumo:** {dados[19] or 'Não preenchido'}"
            )

            st.write(
                f"**Palavras-chave:** {dados[21] or 'Não preenchido'}"
            )

            st.write(
                f"**Referências:** {dados[32] or 'Não preenchido'}"
            )

            st.divider()

            if st.button(
                "↩ Voltar para desenvolvimento",
                key=f"voltar_{id_artigo}"
            ):

                executar("""
                    UPDATE artigos
                    SET
                        status = 'desenvolvimento',
                        data_atualizacao = ?
                    WHERE id = ?
                """, (
                    str(date.today()),
                    id_artigo
                ))

                st.rerun()
