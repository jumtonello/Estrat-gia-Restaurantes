# app.py - Sistema Estratégico para Restaurantes com Autenticação Simples (Streamlit)

import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# =============================================================================
# CONFIGURAÇÃO DE CREDENCIAIS DE LOGIN
# =============================================================================
VALID_USER = "admin"
VALID_PASSWORD = "admin"


def check_password():
    """Exibe o formulário de login e retorna True apenas se as credenciais forem válidas."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        return True

    st.title("🔒 Login")
    st.write("Por favor, informe suas credenciais para acessar o sistema.")

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar")

        if submitted:
            if username == VALID_USER and password == VALID_PASSWORD:
                st.session_state["authenticated"] = True
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

    return False


# =============================================================================
# INÍCIO DO APLICATIVO - SOMENTE APÓS LOGIN
# =============================================================================
if not check_password():
    st.stop()

# -----------------------------------------------------------------------------
# Inicialização do session_state para dados dos módulos
# -----------------------------------------------------------------------------
if "onboarding_data" not in st.session_state:
    st.session_state["onboarding_data"] = {}
if "mercado_data" not in st.session_state:
    st.session_state["mercado_data"] = {}
if "estrategia_data" not in st.session_state:
    st.session_state["estrategia_data"] = {}
if "identidade_data" not in st.session_state:
    st.session_state["identidade_data"] = {}
if "performance_data" not in st.session_state:
    st.session_state["performance_data"] = {}
if "calendario_posts" not in st.session_state:
    st.session_state["calendario_posts"] = []

# -----------------------------------------------------------------------------
# Dados de exemplo das Skills
# -----------------------------------------------------------------------------
SKILLS_DATA = [
    {"Skill": "Comunicação", "Nível": 3, "Última Avaliação": "2024-01-15"},
    {"Skill": "Liderança", "Nível": 4, "Última Avaliação": "2024-02-10"},
    {"Skill": "Pensamento Crítico", "Nível": 2, "Última Avaliação": "2024-03-05"},
    {"Skill": "Trabalho em Equipe", "Nível": 5, "Última Avaliação": "2024-01-20"},
    {"Skill": "Gestão de Tempo", "Nível": 3, "Última Avaliação": "2024-02-25"},
]


def carregar_skills():
    """Retorna um DataFrame com as skills cadastradas."""
    return pd.DataFrame(SKILLS_DATA)


def gerar_relatorio_skills(df):
    """Gera um relatório textual simples das skills."""
    linhas = []
    linhas.append("# Relatório de Skills\n")
    linhas.append(f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
    linhas.append(f"Total de skills avaliadas: {len(df)}\n")
    nivel_medio = df["Nível"].mean()
    linhas.append(f"Nível médio: {nivel_medio:.2f}\n")
    linhas.append("\n## Detalhamento\n")
    for _, row in df.iterrows():
        linhas.append(f"- {row['Skill']}: Nível {row['Nível']} (Última Avaliação: {row['Última Avaliação']})")
    return "\n".join(linhas)


def sugestao_ia(skill, nivel):
    """Retorna uma sugestão de desenvolvimento gerada por 'IA' (simulada)."""
    if nivel <= 2:
        return f"Para '{skill}', foque em treinamentos introdutórios e prática guiada."
    elif nivel == 3:
        return f"Para '{skill}', busque projetos práticos para consolidar o conhecimento."
    else:
        return f"Para '{skill}', considere mentoria e liderança de iniciativas avançadas."


# -----------------------------------------------------------------------------
# Layout principal - Navegação entre módulos estratégicos
# -----------------------------------------------------------------------------
st.title("🍽️ Sistema Estratégico para Restaurantes")
st.sidebar.title("Navegação")
opcao = st.sidebar.radio(
    "Selecione um módulo:",
    [
        "Apresentação",
        "1. Onboarding / DNA",
        "2. Mercado / Persona",
        "3. Estratégia Editorial",
        "4. Identidade / Voz",
        "5. Performance / Calendário",
        "Skills",
    ],
)

# =========================================================================
# APRESENTAÇÃO
# =========================================================================
if opcao == "Apresentação":
    st.header("📌 Apresentação")
    st.write(
        "Bem-vindo ao Sistema Estratégico para Restaurantes! "
        "Este aplicativo reúne 5 módulos estratégicos para estruturar e otimizar "
        "a presença digital e o marketing do seu restaurante, além de integrar "
        "a avaliação de Skills da equipe."
    )

    st.subheader("Módulos Estratégicos")
    st.markdown(
        """
        1. **Onboarding / DNA** — Coleta informações fundamentais do restaurante.
        2. **Mercado / Persona** — Define público-alvo e análise de mercado.
        3. **Estratégia Editorial** — Planeja conteúdos e canais de comunicação.
        4. **Identidade / Voz** — Estabelece tom de voz e identidade visual.
        5. **Performance / Calendário** — Acompanha métricas e organiza o calendário editorial.
        """
    )

    st.subheader("Skills")
    st.write(
        "O módulo de Skills permite cadastrar, visualizar e gerar relatórios "
        "das competências da equipe, além de obter sugestões de desenvolvimento."
    )

    st.info("Use o menu lateral para navegar entre os módulos.")

# =========================================================================
# MÓDULO 1 — ONBOARDING / DNA
# =========================================================================
elif opcao == "1. Onboarding / DNA":
    st.header("🧬 Módulo 1: Onboarding / DNA")
    st.write("Preencha as informações fundamentais do seu restaurante.")

    with st.form("form_onboarding"):
        st.subheader("Dados do Restaurante")
        nome_restaurante = st.text_input("Nome do Restaurante", value=st.session_state["onboarding_data"].get("nome_restaurante", ""))
        tipo_cozinha = st.text_input("Tipo de Cozinha (ex: Italiana, Japonesa, Brasileira)", value=st.session_state["onboarding_data"].get("tipo_cozinha", ""))
        cidade = st.text_input("Cidade", value=st.session_state["onboarding_data"].get("cidade", ""))
        estado = st.text_input("Estado", value=st.session_state["onboarding_data"].get("estado", ""))
        endereco = st.text_input("Endereço", value=st.session_state["onboarding_data"].get("endereco", ""))
        telefone = st.text_input("Telefone", value=st.session_state["onboarding_data"].get("telefone", ""))
        website = st.text_input("Website", value=st.session_state["onboarding_data"].get("website", ""))
        instagram = st.text_input("Instagram", value=st.session_state["onboarding_data"].get("instagram", ""))
        facebook = st.text_input("Facebook", value=st.session_state["onboarding_data"].get("facebook", ""))
        tiktok = st.text_input("TikTok", value=st.session_state["onboarding_data"].get("tiktok", ""))

        st.subheader("Informações Operacionais")
        horario_funcionamento = st.text_area("Horário de Funcionamento", value=st.session_state["onboarding_data"].get("horario_funcionamento", ""))
        capacidade_clientes = st.number_input("Capacidade de Clientes", min_value=0, value=st.session_state["onboarding_data"].get("capacidade_clientes", 0))
        delivery = st.checkbox("Possui Delivery?", value=st.session_state["onboarding_data"].get("delivery", False))
        reservas = st.checkbox("Aceita Reservas?", value=st.session_state["onboarding_data"].get("reservas", False))

        st.subheader("Diferenciais e História")
        ano_fundacao = st.number_input("Ano de Fundação", min_value=1900, max_value=datetime.now().year, value=st.session_state["onboarding_data"].get("ano_fundacao", 2000))
        historia = st.text_area("História do Restaurante", value=st.session_state["onboarding_data"].get("historia", ""))
        diferenciais = st.text_area("Principais Diferenciais", value=st.session_state["onboarding_data"].get("diferenciais", ""))
        pratos_assinatura = st.text_area("Pratos de Assinatura", value=st.session_state["onboarding_data"].get("pratos_assinatura", ""))

        submitted = st.form_submit_button("Salvar Onboarding")
        if submitted:
            st.session_state["onboarding_data"] = {
                "nome_restaurante": nome_restaurante,
                "tipo_cozinha": tipo_cozinha,
                "cidade": cidade,
                "estado": estado,
                "endereco": endereco,
                "telefone": telefone,
                "website": website,
                "instagram": instagram,
                "facebook": facebook,
                "tiktok": tiktok,
                "horario_funcionamento": horario_funcionamento,
                "capacidade_clientes": capacidade_clientes,
                "delivery": delivery,
                "reservas": reservas,
                "ano_fundacao": ano_fundacao,
                "historia": historia,
                "diferenciais": diferenciais,
                "pratos_assinatura": pratos_assinatura,
            }
            st.success("Dados de Onboarding salvos com sucesso!")

    if st.session_state["onboarding_data"]:
        st.subheader("📋 Resumo do Onboarding")
        st.json(st.session_state["onboarding_data"])

# =========================================================================
# MÓDULO 2 — MERCADO / PERSONA
# =========================================================================
elif opcao == "2. Mercado / Persona":
    st.header("🎯 Módulo 2: Mercado / Persona")
    st.write("Defina seu público-alvo e analise o mercado.")

    with st.form("form_mercado"):
        st.subheader("Persona / Público-Alvo")
        nome_persona = st.text_input("Nome da Persona", value=st.session_state["mercado_data"].get("nome_persona", ""))
        idade_persona = st.number_input("Idade", min_value=0, max_value=120, value=st.session_state["mercado_data"].get("idade_persona", 30))
        genero_persona = st.selectbox("Gênero", ["Masculino", "Feminino", "Outro", "Indiferente"], index=["Masculino", "Feminino", "Outro", "Indiferente"].index(st.session_state["mercado_data"].get("genero_persona", "Indiferente")))
        renda_persona = st.selectbox("Faixa de Renda", ["Baixa", "Média", "Média-Alta", "Alta"], index=["Baixa", "Média", "Média-Alta", "Alta"].index(st.session_state["mercado_data"].get("renda_persona", "Média")))
        ocupacao_persona = st.text_input("Ocupação", value=st.session_state["mercado_data"].get("ocupacao_persona", ""))
        interesses_persona = st.text_area("Interesses", value=st.session_state["mercado_data"].get("interesses_persona", ""))
        comportamento_persona = st.text_area("Comportamento Digital", value=st.session_state["mercado_data"].get("comportamento_persona", ""))
        redes_sociais_persona = st.text_area("Redes Sociais que utiliza", value=st.session_state["mercado_data"].get("redes_sociais_persona", ""))

        st.subheader("Análise de Mercado")
        concorrentes = st.text_area("Principais Concorrentes", value=st.session_state["mercado_data"].get("concorrentes", ""))
        vantagem_competitiva = st.text_area("Vantagem Competitiva", value=st.session_state["mercado_data"].get("vantagem_competitiva", ""))
        oportunidades = st.text_area("Oportunidades de Mercado", value=st.session_state["mercado_data"].get("oportunidades", ""))
        ameacas = st.text_area("Ameaças", value=st.session_state["mercado_data"].get("ameacas", ""))

        st.subheader("Posicionamento")
        posicionamento = st.text_area("Posicionamento Desejado", value=st.session_state["mercado_data"].get("posicionamento", ""))
        proposta_valor = st.text_area("Proposta de Valor", value=st.session_state["mercado_data"].get("proposta_valor", ""))

        submitted = st.form_submit_button("Salvar Mercado / Persona")
        if submitted:
            st.session_state["mercado_data"] = {
                "nome_persona": nome_persona,
                "idade_persona": idade_persona,
                "genero_persona": genero_persona,
                "renda_persona": renda_persona,
                "ocupacao_persona": ocupacao_persona,
                "interesses_persona": interesses_persona,
                "comportamento_persona": comportamento_persona,
                "redes_sociais_persona": redes_sociais_persona,
                "concorrentes": concorrentes,
                "vantagem_competitiva": vantagem_competitiva,
                "oportunidades": oportunidades,
                "ameacas": ameacas,
                "posicionamento": posicionamento,
                "proposta_valor": proposta_valor,
            }
            st.success("Dados de Mercado / Persona salvos com sucesso!")

    if st.session_state["mercado_data"]:
        st.subheader("📋 Resumo de Mercado / Persona")
        st.json(st.session_state["mercado_data"])

# =========================================================================
# MÓDULO 3 — ESTRATÉGIA EDITORIAL
# =========================================================================
elif opcao == "3. Estratégia Editorial":
    st.header("📝 Módulo 3: Estratégia Editorial")
    st.write("Planeje os conteúdos e canais de comunicação.")

    with st.form("form_estrategia"):
        st.subheader("Canais de Comunicação")
        canal_instagram = st.checkbox("Instagram", value=st.session_state["estrategia_data"].get("canal_instagram", True))
        canal_facebook = st.checkbox("Facebook", value=st.session_state["estrategia_data"].get("canal_facebook", False))
        canal_tiktok = st.checkbox("TikTok", value=st.session_state["estrategia_data"].get("canal_tiktok", False))
        canal_youtube = st.checkbox("YouTube", value=st.session_state["estrategia_data"].get("canal_youtube", False))
        canal_whatsapp = st.checkbox("WhatsApp", value=st.session_state["estrategia_data"].get("canal_whatsapp", False))
        canal_email = st.checkbox("E-mail Marketing", value=st.session_state["estrategia_data"].get("canal_email", False))
        canal_blog = st.checkbox("Blog / Site", value=st.session_state["estrategia_data"].get("canal_blog", False))

        st.subheader("Frequência de Postagem")
        freq_instagram = st.selectbox("Frequência Instagram", ["Diária", "3x/semana", "2x/semana", "Semanal", "Quinzenal"], index=0)
        freq_facebook = st.selectbox("Frequência Facebook", ["Diária", "3x/semana", "2x/semana", "Semanal", "Quinzenal"], index=2)
        freq_tiktok = st.selectbox("Frequência TikTok", ["Diária", "3x/semana", "2x/semana", "Semanal", "Quinzenal"], index=0)

        st.subheader("Tipos de Conteúdo")
        conteudo_pratos = st.checkbox("Pratos / Cardápio", value=st.session_state["estrategia_data"].get("conteudo_pratos", True))
        conteudo_bastidores = st.checkbox("Bastidores / Cozinha", value=st.session_state["estrategia_data"].get("conteudo_bastidores", True))
        conteudo_promocoes = st.checkbox("Promoções / Ofertas", value=st.session_state["estrategia_data"].get("conteudo_promocoes", True))
        conteudo_educativo = st.checkbox("Educativo / Dicas", value=st.session_state["estrategia_data"].get("conteudo_educativo", False))
        conteudo_ugc = st.checkbox("Conteúdo de Clientes (UGC)", value=st.session_state["estrategia_data"].get("conteudo_ugc", False))
        conteudo_eventos = st.checkbox("Eventos / Novidades", value=st.session_state["estrategia_data"].get("conteudo_eventos", True))

        st.subheader("Objetivos")
        objetivo_principal = st.selectbox("Objetivo Principal", ["Aumentar Reconhecimento", "Gerar Engajamento", "Atrair Clientes", "Fidelizar Clientes", "Vendas Online"], index=0)
        meta_seguidores = st.number_input("Meta de Seguidores (mensal)", min_value=0, value=st.session_state["estrategia_data"].get("meta_seguidores", 100))
        meta_engajamento = st.slider("Meta de Engajamento (%)", 0, 100, st.session_state["estrategia_data"].get("meta_engajamento", 5))

        st.subheader("Estratégia Geral")
        estrategia_geral = st.text_area("Descreva a estratégia editorial", value=st.session_state["estrategia_data"].get("estrategia_geral", ""))

        submitted = st.form_submit_button("Salvar Estratégia Editorial")
        if submitted:
            st.session_state["estrategia_data"] = {
                "canal_instagram": canal_instagram,
                "canal_facebook": canal_facebook,
                "canal_tiktok": canal_tiktok,
                "canal_youtube": canal_youtube,
                "canal_whatsapp": canal_whatsapp,
                "canal_email": canal_email,
                "canal_blog": canal_blog,
                "freq_instagram": freq_instagram,
                "freq_facebook": freq_facebook,
                "freq_tiktok": freq_tiktok,
                "conteudo_pratos": conteudo_pratos,
                "conteudo_bastidores": conteudo_bastidores,
                "conteudo_promocoes": conteudo_promocoes,
                "conteudo_educativo": conteudo_educativo,
                "conteudo_ugc": conteudo_ugc,
                "conteudo_eventos": conteudo_eventos,
                "objetivo_principal": objetivo_principal,
                "meta_seguidores": meta_seguidores,
                "meta_engajamento": meta_engajamento,
                "estrategia_geral": estrategia_geral,
            }
            st.success("Estratégia Editorial salva com sucesso!")

    if st.session_state["estrategia_data"]:
        st.subheader("📋 Resumo da Estratégia Editorial")
        st.json(st.session_state["estrategia_data"])

# =========================================================================
# MÓDULO 4 — IDENTIDADE / VOZ
# =========================================================================
elif opcao == "4. Identidade / Voz":
    st.header("🎨 Módulo 4: Identidade / Voz")
    st.write("Estabeleça o tom de voz e a identidade visual do restaurante.")

    with st.form("form_identidade"):
        st.subheader("Tom de Voz")
        tom_voz = st.selectbox("Tom de Voz Principal", ["Formal", "Descontraído", "Amigável", "Sofisticado", "Divertido", "Inspirador"], index=2)
        tom_secundario = st.selectbox("Tom de Voz Secundário", ["Nenhum", "Formal", "Descontraído", "Amigável", "Sofisticado", "Divertido", "Inspirador"], index=0)
        linguagem = st.selectbox("Linguagem", ["Simples e Acessível", "Técnica", "Regional/Gírias", "Premium/Refinada"], index=0)
        pronome = st.selectbox("Tratamento", ["Você", "Tu", "Vós"], index=0)

        st.subheader("Identidade Visual")
        cor_primaria = st.color_picker("Cor Primária", value=st.session_state["identidade_data"].get("cor_primaria", "#FF6B35"))
        cor_secundaria = st.color_picker("Cor Secundária", value=st.session_state["identidade_data"].get("cor_secundaria", "#F7C59F"))
        cor_destaque = st.color_picker("Cor de Destaque", value=st.session_state["identidade_data"].get("cor_destaque", "#004E89"))
        estilo_fotografia = st.selectbox("Estilo de Fotografia", ["Minimalista", "Rústico", "Gourmet/Profissional", "Vibrante/Colorido", "Dark/Mood"], index=2)
        fonte_estilo = st.selectbox("Estilo de Fonte", ["Serifada (Clássica)", "Sem Serifa (Moderna)", "Manuscrita (Artesanal)", "Display (Impactante)"], index=1)

        st.subheader("Palavras-Chave e Conceitos")
        palavras_chave = st.text_area("Palavras-Chave da Marca", value=st.session_state["identidade_data"].get("palavras_chave", ""))
        palavras_evitar = st.text_area("Palavras a Evitar", value=st.session_state["identidade_data"].get("palavras_evitar", ""))
        slogan = st.text_input("Slogan / Tagline", value=st.session_state["identidade_data"].get("slogan", ""))
        missao = st.text_area("Missão", value=st.session_state["identidade_data"].get("missao", ""))
        visao = st.text_area("Visão", value=st.session_state["identidade_data"].get("visao", ""))
        valores = st.text_area("Valores", value=st.session_state["identidade_data"].get("valores", ""))

        st.subheader("Diretrizes de Conteúdo")
        diretrizes = st.text_area("Diretrizes de Comunicação", value=st.session_state["identidade_data"].get("diretrizes", ""))
        hashtags_padrao = st.text_area("Hashtags Padrão", value=st.session_state["identidade_data"].get("hashtags_padrao", ""))

        submitted = st.form_submit_button("Salvar Identidade / Voz")
        if submitted:
            st.session_state["identidade_data"] = {
                "tom_voz": tom_voz,
                "tom_secundario": tom_secundario,
                "linguagem": linguagem,
                "pronome": pronome,
                "cor_primaria": cor_primaria,
                "cor_secundaria": cor_secundaria,
                "cor_destaque": cor_destaque,
                "estilo_fotografia": estilo_fotografia,
                "fonte_estilo": fonte_estilo,
                "palavras_chave": palavras_chave,
                "palavras_evitar": palavras_evitar,
                "slogan": slogan,
                "missao": missao,
                "visao": visao,
                "valores": valores,
                "diretrizes": diretrizes,
                "hashtags_padrao": hashtags_padrao,
            }
            st.success("Identidade / Voz salvas com sucesso!")

    if st.session_state["identidade_data"]:
        st.subheader("📋 Resumo de Identidade / Voz")
        st.json(st.session_state["identidade_data"])

        st.subheader("🎨 Preview de Cores")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.color_picker("Primária", st.session_state["identidade_data"]["cor_primaria"])
        with col2:
            st.color_picker("Secundária", st.session_state["identidade_data"]["cor_secundaria"])
        with col3:
            st.color_picker("Destaque", st.session_state["identidade_data"]["cor_destaque"])

# =========================================================================
# MÓDULO 5 — PERFORMANCE / CALENDÁRIO
# =========================================================================
elif opcao == "5. Performance / Calendário":
    st.header("📈 Módulo 5: Performance / Calendário")
    st.write("Acompanhe métricas e organize o calendário editorial.")

    tab_performance, tab_calendario = st.tabs(["📊 Performance", "📅 Calendário Editorial"])

    # --- Tab Performance ---
    with tab_performance:
        st.subheader("Métricas de Performance")
        with st.form("form_performance"):
            col1, col2 = st.columns(2)
            with col1:
                seguidores_instagram = st.number_input("Seguidores Instagram", min_value=0, value=st.session_state["performance_data"].get("seguidores_instagram", 0))
                seguidores_facebook = st.number_input("Seguidores Facebook", min_value=0, value=st.session_state["performance_data"].get("seguidores_facebook", 0))
                seguidores_tiktok = st.number_input("Seguidores TikTok", min_value=0, value=st.session_state["performance_data"].get("seguidores_tiktok", 0))
                alcance_mensal = st.number_input("Alcance Mensal", min_value=0, value=st.session_state["performance_data"].get("alcance_mensal", 0))

            with col2:
                engajamento_medio = st.slider("Engajamento Médio (%)", 0, 100, st.session_state["performance_data"].get("engajamento_medio", 0))
                posts_mes = st.number_input("Posts no Mês", min_value=0, value=st.session_state["performance_data"].get("posts_mes", 0))
                cliques_link = st.number_input("Cliques no Link", min_value=0, value=st.session_state["performance_data"].get("cliques_link", 0))
                conversao_delivery = st.slider("Conversão Delivery (%)", 0, 100, st.session_state["performance_data"].get("conversao_delivery", 0))

            periodo_referencia = st.selectbox("Período de Referência", ["Última semana", "Últimos 15 dias", "Último mês", "Últimos 3 meses"], index=2)
            observacoes = st.text_area("Observações", value=st.session_state["performance_data"].get("observacoes", ""))

            submitted = st.form_submit_button("Salvar Performance")
            if submitted:
                st.session_state["performance_data"] = {
                    "seguidores_instagram": seguidores_instagram,
                    "seguidores_facebook": seguidores_facebook,
                    "seguidores_tiktok": seguidores_tiktok,
                    "alcance_mensal": alcance_mensal,
                    "engajamento_medio": engajamento_medio,
                    "posts_mes": posts_mes,
                    "cliques_link": cliques_link,
                    "conversao_delivery": conversao_delivery,
                    "periodo_referencia": periodo_referencia,
                    "observacoes": observacoes,
                }
                st.success("Dados de Performance salvos com sucesso!")

        if st.session_state["performance_data"]:
            st.subheader("📋 Resumo de Performance")
            st.json(st.session_state["performance_data"])

    # --- Tab Calendário ---
    with tab_calendario:
        st.subheader("📅 Calendário Editorial")
        st.write("Adicione e visualize os posts planejados.")

        with st.form("form_calendario"):
            col1, col2 = st.columns(2)
            with col1:
                data_post = st.date_input("Data do Post", datetime.now())
                canal_post = st.selectbox("Canal", ["Instagram", "Facebook", "TikTok", "YouTube", "WhatsApp", "E-mail", "Blog/Site"])
                tipo_conteudo = st.selectbox("Tipo de Conteúdo", ["Prato/Cardápio", "Bastidores", "Promoção", "Educativo", "UGC", "Evento", "Story", "Reels"])

            with col2:
                titulo_post = st.text_input("Título / Tema do Post")
                horario_post = st.time_input("Horário", datetime.now().time())
                status_post = st.selectbox("Status", ["Planejado", "Em Produção", "Pronto", "Publicado"])

            descricao_post = st.text_area("Descrição / Roteiro")
            hashtags_post = st.text_input("Hashtags")
            responsavel = st.text_input("Responsável")

            submitted = st.form_submit_button("Adicionar ao Calendário")
            if submitted and titulo_post:
                st.session_state["calendario_posts"].append({
                    "Data": data_post.strftime("%Y-%m-%d"),
                    "Horário": horario_post.strftime("%H:%M"),
                    "Canal": canal_post,
                    "Tipo": tipo_conteudo,
                    "Título": titulo_post,
                    "Status": status_post,
                    "Responsável": responsavel,
                    "Hashtags": hashtags_post,
                    "Descrição": descricao_post,
                })
                st.success(f"Post '{titulo_post}' adicionado ao calendário!")

        if st.session_state["calendario_posts"]:
            st.subheader("📋 Posts Planejados")
            df_calendario = pd.DataFrame(st.session_state["calendario_posts"])
            st.dataframe(df_calendario, use_container_width=True)

            st.subheader("Exportar Calendário")
            st.download_button(
                label="⬇️ Baixar calendário (.csv)",
                data=df_calendario.to_csv(index=False).encode("utf-8"),
                file_name=f"calendario_editorial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
            )
        else:
            st.info("Nenhum post adicionado ao calendário ainda.")

# =========================================================================
# SKILLS
# =========================================================================
elif opcao == "Skills":
    st.header("🧠 Skills")
    st.write("Gerencie as competências da equipe do restaurante.")

    df = carregar_skills()
    st.dataframe(df, use_container_width=True)

    st.subheader("➕ Adicionar nova Skill")
    with st.form("form_skill"):
        nova_skill = st.text_input("Nome da Skill")
        novo_nivel = st.slider("Nível (1-5)", 1, 5, 3)
        data_avaliacao = st.date_input("Data da Avaliação", datetime.now())
        adicionar = st.form_submit_button("Adicionar")
        if adicionar and nova_skill:
            SKILLS_DATA.append(
                {
                    "Skill": nova_skill,
                    "Nível": novo_nivel,
                    "Última Avaliação": data_avaliacao.strftime("%Y-%m-%d"),
                }
            )
            st.success(f"Skill '{nova_skill}' adicionada com sucesso!")
            st.rerun()

    st.subheader("🤖 Sugestões de IA")
    df = carregar_skills()
    for _, row in df.iterrows():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{row['Skill']}** - Nível {row['Nível']}")
        with col2:
            if st.button("Sugestão IA", key=f"ia_{row['Skill']}"):
                st.info(sugestao_ia(row["Skill"], row["Nível"]))

    st.subheader("📄 Relatório de Skills")
    relatorio = gerar_relatorio_skills(df)
    st.text(relatorio)

    st.subheader("Exportar")
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        st.download_button(
            label="⬇️ Baixar relatório (.txt)",
            data=relatorio,
            file_name=f"relatorio_skills_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
        )
    with col_exp2:
        st.download_button(
            label="⬇️ Baixar dados (.csv)",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name=f"skills_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )
