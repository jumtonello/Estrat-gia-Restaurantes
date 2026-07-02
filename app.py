# app.py - Sistema Estratégico para Restaurantes com Autenticação Simples (Streamlit)
# Suporta múltiplos restaurantes com persistência em database.json
# Inclui botão 'Processar com IA' em cada módulo estratégico

import os
import json
import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# =============================================================================
# CONFIGURAÇÃO DE CREDENCIAIS DE LOGIN
# =============================================================================
VALID_USER = "admin"
VALID_PASSWORD = "admin"

DATABASE_FILE = "database.json"

DEFAULT_SKILLS = [
    {"Skill": "Comunicação", "Nível": 3, "Última Avaliação": "2024-01-15"},
    {"Skill": "Liderança", "Nível": 4, "Última Avaliação": "2024-02-10"},
    {"Skill": "Pensamento Crítico", "Nível": 2, "Última Avaliação": "2024-03-05"},
    {"Skill": "Trabalho em Equipe", "Nível": 5, "Última Avaliação": "2024-01-20"},
    {"Skill": "Gestão de Tempo", "Nível": 3, "Última Avaliação": "2024-02-25"},
]


def empty_restaurant_data():
    """Retorna a estrutura padrão de dados para um restaurante."""
    return {
        "onboarding_data": {},
        "mercado_data": {},
        "estrategia_data": {},
        "identidade_data": {},
        "performance_data": {},
        "calendario_posts": [],
        "skills_data": [dict(s) for s in DEFAULT_SKILLS],
    }


def load_database():
    """Carrega o arquivo database.json. Retorna estrutura vazia se não existir."""
    if os.path.exists(DATABASE_FILE):
        try:
            with open(DATABASE_FILE, "r", encoding="utf-8") as f:
                db = json.load(f)
            if "restaurants" not in db or not isinstance(db["restaurants"], dict):
                db["restaurants"] = {}
            return db
        except (json.JSONDecodeError, OSError):
            return {"restaurants": {}}
    return {"restaurants": {}}


def save_database(db):
    """Salva a estrutura de dados no arquivo database.json."""
    with open(DATABASE_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def apply_restaurant_data(name):
    """Carrega os dados do restaurante selecionado para o session_state."""
    db = load_database()
    data = db["restaurants"].get(name, empty_restaurant_data())
    for key, default in empty_restaurant_data().items():
        st.session_state[key] = data.get(key, default)


def persist_current_restaurant():
    """Persiste os dados atuais do session_state no database.json."""
    name = st.session_state.get("current_restaurant")
    if not name:
        return
    db = load_database()
    db["restaurants"][name] = {
        key: st.session_state.get(key, default)
        for key, default in empty_restaurant_data().items()
    }
    save_database(db)


def safe_index(options, value, default=0):
    """Retorna o índice seguro de um valor em uma lista de opções."""
    return options.index(value) if value in options else default


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


def processar_com_ia(modulo, dados):
    """
    Processa os dados do módulo informado utilizando as informações salvas
    no session_state do restaurante selecionado e retorna uma análise
    estratégica simulada por IA.
    """
    restaurante = st.session_state.get("current_restaurant", "Restaurante")
    linhas = []
    linhas.append(f"🤖 Análise de IA — {modulo}")
    linhas.append(f"Restaurante: {restaurante}")
    linhas.append(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    linhas.append("")

    if not dados:
        linhas.append("⚠️ Não há dados salvos para este módulo.")
        linhas.append("Preencha e salve o formulário antes de processar com IA.")
        return "\n".join(linhas)

    if modulo == "Onboarding / DNA":
        linhas.append("📌 Resumo do DNA do Restaurante:")
        linhas.append(f"- Nome: {dados.get('nome_restaurante', 'N/D')}")
        linhas.append(f"- Cozinha: {dados.get('tipo_cozinha', 'N/D')}")
        linhas.append(f"- Localização: {dados.get('cidade', 'N/D')}/{dados.get('estado', 'N/D')}")
        linhas.append(f"- Diferenciais: {dados.get('diferenciais', 'N/D')}")
        linhas.append("")
        linhas.append("💡 Recomendações de IA:")
        linhas.append("- Destaque os pratos de assinatura nas redes sociais.")
        linhas.append("- Use a história do restaurante para criar conexão emocional.")
        linhas.append("- Reforce os diferenciais competitivos em campanhas sazonais.")

    elif modulo == "Mercado / Persona":
        linhas.append("🎯 Análise de Mercado e Persona:")
        linhas.append(f"- Persona: {dados.get('nome_persona', 'N/D')} ({dados.get('idade_persona', 'N/D')} anos)")
        linhas.append(f"- Renda: {dados.get('renda_persona', 'N/D')}")
        linhas.append(f"- Posicionamento: {dados.get('posicionamento', 'N/D')}")
        linhas.append("")
        linhas.append("💡 Recomendações de IA:")
        linhas.append("- Direcione conteúdos para os interesses da persona definida.")
        linhas.append("- Explore a vantagem competitiva nas mensagens principais.")
        linhas.append("- Crie ações específicas para as oportunidades identificadas.")

    elif modulo == "Estratégia Editorial":
        canais = []
        if dados.get("canal_instagram"): canais.append("Instagram")
        if dados.get("canal_facebook"): canais.append("Facebook")
        if dados.get("canal_tiktok"): canais.append("TikTok")
        if dados.get("canal_youtube"): canais.append("YouTube")
        if dados.get("canal_whatsapp"): canais.append("WhatsApp")
        linhas.append("📝 Análise da Estratégia Editorial:")
        linhas.append(f"- Canais ativos: {', '.join(canais) if canais else 'Nenhum'}")
        linhas.append(f"- Objetivo principal: {dados.get('objetivo_principal', 'N/D')}")
        linhas.append(f"- Meta de seguidores: {dados.get('meta_seguidores', 0)}")
        linhas.append(f"- Meta de engajamento: {dados.get('meta_engajamento', 0)}%")
        linhas.append("")
        linhas.append("💡 Recomendações de IA:")
        linhas.append("- Mantenha consistência na frequência de postagem em cada canal.")
        linhas.append("- Diversifique os tipos de conteúdo para manter o engajamento.")
        linhas.append("- Acompanhe semanalmente a evolução das metas definidas.")

    elif modulo == "Identidade / Voz":
        linhas.append("🎨 Análise de Identidade / Voz:")
        linhas.append(f"- Tom de voz: {dados.get('tom_voz', 'N/D')}")
        linhas.append(f"- Linguagem: {dados.get('linguagem', 'N/D')}")
        linhas.append(f"- Slogan: {dados.get('slogan', 'N/D')}")
        linhas.append(f"- Palavras-chave: {dados.get('palavras_chave', 'N/D')}")
        linhas.append("")
        linhas.append("💡 Recomendações de IA:")
        linhas.append("- Padronize o tom de voz em todos os pontos de contato.")
        linhas.append("- Use as cores definidas como base para todo material visual.")
        linhas.append("- Evite as palavras listadas e reforce as palavras-chave da marca.")

    elif modulo == "Performance / Calendário":
        linhas.append("📈 Análise de Performance:")
        linhas.append(f"- Seguidores Instagram: {dados.get('seguidores_instagram', 0)}")
        linhas.append(f"- Engajamento médio: {dados.get('engajamento_medio', 0)}%")
        linhas.append(f"- Posts no mês: {dados.get('posts_mes', 0)}")
        linhas.append(f"- Conversão delivery: {dados.get('conversao_delivery', 0)}%")
        linhas.append("")
        linhas.append("💡 Recomendações de IA:")
        linhas.append("- Identifique os canais com melhor desempenho e invista mais neles.")
        linhas.append("- Ajuste a frequência de posts com base no engajamento observado.")
        linhas.append("- Use o calendário editorial para garantir consistência e planejamento.")

    else:
        linhas.append("Módulo não reconhecido para processamento de IA.")

    return "\n".join(linhas)


def gerar_apresentacao_geral():
    """Consolida os dados de todos os módulos para uma apresentação final."""
    restaurante = st.session_state.get("current_restaurant", "Restaurante")
    onboarding = st.session_state.get("onboarding_data", {})
    mercado = st.session_state.get("mercado_data", {})
    estrategia = st.session_state.get("estrategia_data", {})
    identidade = st.session_state.get("identidade_data", {})
    performance = st.session_state.get("performance_data", {})

    linhas = []
    linhas.append(f"# Apresentação Estratégica — {restaurante}")
    linhas.append(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    linhas.append("")
    linhas.append("## 1. Onboarding / DNA")
    linhas.append(f"- Cozinha: {onboarding.get('tipo_cozinha', 'N/D')}")
    linhas.append(f"- Cidade: {onboarding.get('cidade', 'N/D')}/{onboarding.get('estado', 'N/D')}")
    linhas.append(f"- Diferenciais: {onboarding.get('diferenciais', 'N/D')}")
    linhas.append("")
    linhas.append("## 2. Mercado / Persona")
    linhas.append(f"- Persona: {mercado.get('nome_persona', 'N/D')}")
    linhas.append(f"- Posicionamento: {mercado.get('posicionamento', 'N/D')}")
    linhas.append(f"- Proposta de valor: {mercado.get('proposta_valor', 'N/D')}")
    linhas.append("")
    linhas.append("## 3. Estratégia Editorial")
    linhas.append(f"- Objetivo: {estrategia.get('objetivo_principal', 'N/D')}")
    linhas.append(f"- Meta de seguidores: {estrategia.get('meta_seguidores', 0)}")
    linhas.append(f"- Meta de engajamento: {estrategia.get('meta_engajamento', 0)}%")
    linhas.append("")
    linhas.append("## 4. Identidade / Voz")
    linhas.append(f"- Tom de voz: {identidade.get('tom_voz', 'N/D')}")
    linhas.append(f"- Slogan: {identidade.get('slogan', 'N/D')}")
    linhas.append(f"- Palavras-chave: {identidade.get('palavras_chave', 'N/D')}")
    linhas.append("")
    linhas.append("## 5. Performance / Calendário")
    linhas.append(f"- Seguidores Instagram: {performance.get('seguidores_instagram', 0)}")
    linhas.append(f"- Engajamento médio: {performance.get('engajamento_medio', 0)}%")
    linhas.append(f"- Posts no mês: {performance.get('posts_mes', 0)}")
    linhas.append("")
    linhas.append("---")
    linhas.append("Apresentação gerada pelo Sistema Estratégico para Restaurantes.")
    return "\n".join(linhas)


# =============================================================================
# INÍCIO DO APLICATIVO - SOMENTE APÓS LOGIN
# =============================================================================
if not check_password():
    st.stop()

# -----------------------------------------------------------------------------
# Inicialização do session_state para dados dos módulos
# -----------------------------------------------------------------------------
if "current_restaurant" not in st.session_state:
    st.session_state["current_restaurant"] = None

for key, default in empty_restaurant_data().items():
    if key not in st.session_state:
        st.session_state[key] = default

# -----------------------------------------------------------------------------
# Gerenciamento de múltiplos restaurantes com persistência
# -----------------------------------------------------------------------------
db = load_database()
restaurant_names = list(db["restaurants"].keys())

# Carregar automaticamente o primeiro restaurante disponível ao iniciar
if st.session_state["current_restaurant"] is None and restaurant_names:
    st.session_state["current_restaurant"] = restaurant_names[0]
    apply_restaurant_data(restaurant_names[0])
    st.rerun()

# Seletor de restaurante na barra lateral
options = restaurant_names + ["Criar Novo Restaurante"]
current = st.session_state.get("current_restaurant")
if current and current in restaurant_names:
    default_index = options.index(current)
else:
    default_index = len(options) - 1

st.sidebar.title("Restaurantes")
selected = st.sidebar.selectbox(
    "Selecione um restaurante",
    options,
    index=default_index,
    key="restaurant_selector",
)

if selected == "Criar Novo Restaurante":
    st.sidebar.markdown("### Criar Novo Restaurante")
    novo_nome = st.sidebar.text_input(
        "Nome do novo restaurante",
        key="novo_restaurante_nome",
    )
    if st.sidebar.button("Criar Restaurante"):
        if not novo_nome.strip():
            st.sidebar.error("Informe um nome válido.")
        elif novo_nome in db["restaurants"]:
            st.sidebar.error("Já existe um restaurante com esse nome.")
        else:
            db["restaurants"][novo_nome] = empty_restaurant_data()
            save_database(db)
            st.session_state["current_restaurant"] = novo_nome
            apply_restaurant_data(novo_nome)
            st.rerun()

    st.title("🍽️ Sistema Estratégico para Restaurantes")
    st.info("Crie um novo restaurante ou selecione um existente na barra lateral para começar.")
    st.stop()

# Troca de restaurante existente: carrega os dados salvos e recarrega a página
if current != selected:
    st.session_state["current_restaurant"] = selected
    apply_restaurant_data(selected)
    st.rerun()

# -----------------------------------------------------------------------------
# Funções auxiliares de Skills
# -----------------------------------------------------------------------------
def carregar_skills():
    """Retorna um DataFrame com as skills cadastradas do restaurante atual."""
    return pd.DataFrame(st.session_state.get("skills_data", []))


def gerar_relatorio_skills(df):
    """Gera um relatório textual simples das skills."""
    linhas = []
    linhas.append("# Relatório de Skills\n")
    linhas.append(f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
    linhas.append(f"Total de skills avaliadas: {len(df)}\n")
    if len(df) > 0:
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
if current:
    st.caption(f"Restaurante atual: **{current}")

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

    st.info("Use o menu lateral para navegar entre os módulos. Os dados são salvos automaticamente em database.json.")

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

    st.subheader("🤖 Processar com IA")
    if st.button("Processar com IA", key="btn_ia_onboarding"):
        resultado = processar_com_ia("Onboarding / DNA", st.session_state.get("onboarding_data", {}))
        st.text_area("Resultado da IA", value=resultado, height=300, key="ia_result_onboarding")

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
        genero_options = ["Masculino", "Feminino", "Outro", "Indiferente"]
        genero_persona = st.selectbox("Gênero", genero_options, index=safe_index(genero_options, st.session_state["mercado_data"].get("genero_persona", "Indiferente")))
        renda_options = ["Baixa", "Média", "Média-Alta", "Alta"]
        renda_persona = st.selectbox("Faixa de Renda", renda_options, index=safe_index(renda_options, st.session_state["mercado_data"].get("renda_persona", "Média")))
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

    st.subheader("🤖 Processar com IA")
    if st.button("Processar com IA", key="btn_ia_mercado"):
        resultado = processar_com_ia("Mercado / Persona", st.session_state.get("mercado_data", {}))
        st.text_area("Resultado da IA", value=resultado, height=300, key="ia_result_mercado")

# =========================================================================
# MÓDULO 3 — ESTRATÉGIA EDITORIAL
# =========================================================================
elif opcao == "3. Estratégia Editorial":
    st.header("📝 Módulo 3: Estratégia Editorial")
    st.write("Planeje os conteúdos e canais de comunicação.")

    freq_options = ["Diária", "3x/semana", "2x/semana", "Semanal", "Quinzenal"]
    objetivo_options = ["Aumentar Reconhecimento", "Gerar Engajamento", "Atrair Clientes", "Fidelizar Clientes", "Vendas Online"]

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
        freq_instagram = st.selectbox("Frequência Instagram", freq_options, index=safe_index(freq_options, st.session_state["estrategia_data"].get("freq_instagram", "Diária")))
        freq_facebook = st.selectbox("Frequência Facebook", freq_options, index=safe_index(freq_options, st.session_state["estrategia_data"].get("freq_facebook", "2x/semana")))
        freq_tiktok = st.selectbox("Frequência TikTok", freq_options, index=safe_index(freq_options, st.session_state["estrategia_data"].get("freq_tiktok", "Diária")))

        st.subheader("Tipos de Conteúdo")
        conteudo_pratos = st.checkbox("Pratos / Cardápio", value=st.session_state["estrategia_data"].get("conteudo_pratos", True))
        conteudo_bastidores = st.checkbox("Bastidores / Cozinha", value=st.session_state["estrategia_data"].get("conteudo_bastidores", True))
        conteudo_promocoes = st.checkbox("Promoções / Ofertas", value=st.session_state["estrategia_data"].get("conteudo_promocoes", True))
        conteudo_educativo = st.checkbox("Educativo / Dicas", value=st.session_state["estrategia_data"].get("conteudo_educativo", False))
        conteudo_ugc = st.checkbox("Conteúdo de Clientes (UGC)", value=st.session_state["estrategia_data"].get("conteudo_ugc", False))
        conteudo_eventos = st.checkbox("Eventos / Novidades", value=st.session_state["estrategia_data"].get("conteudo_eventos", True))

        st.subheader("Objetivos")
        objetivo_principal = st.selectbox("Objetivo Principal", objetivo_options, index=safe_index(objetivo_options, st.session_state["estrategia_data"].get("objetivo_principal", "Aumentar Reconhecimento")))
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

    st.subheader("🤖 Processar com IA")
    if st.button("Processar com IA", key="btn_ia_estrategia"):
        resultado = processar_com_ia("Estratégia Editorial", st.session_state.get("estrategia_data", {}))
        st.text_area("Resultado da IA", value=resultado, height=300, key="ia_result_estrategia")

# =========================================================================
# MÓDULO 4 — IDENTIDADE / VOZ
# =========================================================================
elif opcao == "4. Identidade / Voz":
    st.header("🎨 Módulo 4: Identidade / Voz")
    st.write("Estabeleça o tom de voz e a identidade visual do restaurante.")

    tom_options = ["Formal", "Descontraído", "Amigável", "Sofisticado", "Divertido", "Inspirador"]
    tom_sec_options = ["Nenhum"] + tom_options
    linguagem_options = ["Simples e Acessível", "Técnica", "Regional/Gírias", "Premium/Refinada"]
    pronome_options = ["Você", "Tu", "Vós"]
    fotografia_options = ["Minimalista", "Rústico", "Gourmet/Profissional", "Vibrante/Colorido", "Dark/Mood"]
    fonte_options = ["Serifada (Clássica)", "Sem Serifa (Moderna)", "Manuscrita (Artesanal)", "Display (Impactante)"]

    with st.form("form_identidade"):
        st.subheader("Tom de Voz")
        tom_voz = st.selectbox("Tom de Voz Principal", tom_options, index=safe_index(tom_options, st.session_state["identidade_data"].get("tom_voz", "Amigável")))
        tom_secundario = st.selectbox("Tom de Voz Secundário", tom_sec_options, index=safe_index(tom_sec_options, st.session_state["identidade_data"].get("tom_secundario", "Nenhum")))
        linguagem = st.selectbox("Linguagem", linguagem_options, index=safe_index(linguagem_options, st.session_state["identidade_data"].get("linguagem", "Simples e Acessível")))
        pronome = st.selectbox("Tratamento", pronome_options, index=safe_index(pronome_options, st.session_state["identidade_data"].get("pronome", "Você")))

        st.subheader("Identidade Visual")
        cor_primaria = st.color_picker("Cor Primária", value=st.session_state["identidade_data"].get("cor_primaria", "#FF6B35"))
        cor_secundaria = st.color_picker("Cor Secundária", value=st.session_state["identidade_data"].get("cor_secundaria", "#F7C59F"))
        cor_destaque = st.color_picker("Cor de Destaque", value=st.session_state["identidade_data"].get("cor_destaque", "#004E89"))
        estilo_fotografia = st.selectbox("Estilo de Fotografia", fotografia_options, index=safe_index(fotografia_options, st.session_state["identidade_data"].get("estilo_fotografia", "Gourmet/Profissional")))
        fonte_estilo = st.selectbox("Estilo de Fonte", fonte_options, index=safe_index(fonte_options, st.session_state["identidade_data"].get("fonte_estilo", "Sem Serifa (Moderna)")))

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

    st.subheader("🤖 Processar com IA")
    if st.button("Processar com IA", key="btn_ia_identidade"):
        resultado = processar_com_ia("Identidade / Voz", st.session_state.get("identidade_data", {}))
        st.text_area("Resultado da IA", value=resultado, height=300, key="ia_result_identidade")

# =========================================================================
# MÓDULO 5 — PERFORMANCE / CALENDÁRIO
# =========================================================================
elif opcao == "5. Performance / Calendário":
    st.header("📈 Módulo 5: Performance / Calendário")
    st.write("Acompanhe métricas e organize o calendário editorial.")

    tab_performance, tab_calendario, tab_apresentacao = st.tabs(["📊 Performance", "📅 Calendário Editorial", "🎤 Apresentação"])

    periodo_options = ["Última semana", "Últimos 15 dias", "Último mês", "Últimos 3 meses"]

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

            periodo_referencia = st.selectbox("Período de Referência", periodo_options, index=safe_index(periodo_options, st.session_state["performance_data"].get("periodo_referencia", "Último mês")))
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

        st.subheader("🤖 Processar com IA")
        if st.button("Processar com IA", key="btn_ia_performance"):
            resultado = processar_com_ia("Performance / Calendário", st.session_state.get("performance_data", {}))
            st.text_area("Resultado da IA", value=resultado, height=300, key="ia_result_performance")

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

    # --- Tab Apresentação ---
    with tab_apresentacao:
        st.subheader("🎤 Apresentação Final")
        st.write("Gere uma apresentação consolidada de todos os módulos estratégicos do restaurante atual.")
        if st.button("Gerar Apresentação", key="btn_apresentacao"):
            apresentacao = gerar_apresentacao_geral()
            st.text_area("Apresentação Estratégica", value=apresentacao, height=500, key="apresentacao_result")
            st.download_button(
                label="⬇️ Baixar apresentação (.txt)",
                data=apresentacao,
                file_name=f"apresentacao_{st.session_state.get('current_restaurant', 'restaurante')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
            )

# =========================================================================
# SKILLS
# =========================================================================
elif opcao == "Skills":
    st.header("🧠 Skills")
    st.write("Gerencie as competências da equipe do restaurante.")

    df = carregar_skills()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Nenhuma skill cadastrada ainda.")

    st.subheader("➕ Adicionar nova Skill")
    with st.form("form_skill"):
        nova_skill = st.text_input("Nome da Skill")
        novo_nivel = st.slider("Nível (1-5)", 1, 5, 3)
        data_avaliacao = st.date_input("Data da Avaliação", datetime.now())
        adicionar = st.form_submit_button("Adicionar")
        if adicionar and nova_skill:
            st.session_state["skills_data"].append(
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
            data=df.to_csv(index=False).encode("utf-8") if not df.empty else b"",
            file_name=f"skills_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )

# -----------------------------------------------------------------------------
# Persistência automática dos dados do restaurante atual ao final da execução
# -----------------------------------------------------------------------------
if st.session_state.get("current_restaurant"):
    persist_current_restaurant()
