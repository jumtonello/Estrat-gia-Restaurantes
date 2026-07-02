import streamlit as st
import json
from datetime import datetime

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Plataforma Estratégica com IA",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# DEFINIÇÃO DAS 5 SKILLS
# Cada Skill possui um identificador, nome, descrição e instruções que orientam
# a geração de insights automáticos pela função 'processar_com_ia'.
# ==============================================================================
SKILLS = {
    "#Arquiteto": {
        "nome": "Arquiteto",
        "descricao": "Estrutura a fundação do projeto, definindo escopo, objetivos e arquitetura.",
        "instrucoes": (
            "Analise os dados de escopo e objetivos fornecidos. Identifique pilares estruturais, "
            "dependências críticas e proponha uma arquitetura lógica para o projeto."
        ),
    },
    "#Inteligência": {
        "nome": "Inteligência",
        "descricao": "Coleta e organiza informações relevantes do contexto e do mercado.",
        "instrucoes": (
            "Avalie as informações de contexto e mercado inseridas. Destaque tendências, "
            "riscos informacionais e oportunidades de inteligência competitiva."
        ),
    },
    "#Estrategista": {
        "nome": "Estrategista",
        "descricao": "Define estratégias, prioridades e plano de ação.",
        "instrucoes": (
            "Com base nos objetivos e no contexto, formule estratégias prioritárias, "
            "defina métricas de sucesso e sugira um plano de ação estruturado."
        ),
    },
    "#Curador": {
        "nome": "Curador",
        "descricao": "Seleciona, organiza e valida conteúdos e recursos relevantes.",
        "instrucoes": (
            "Revise os conteúdos e recursos informados. Selecione os mais relevantes, "
            "identifique lacunas de conteúdo e proponha uma curadoria organizada por temas."
        ),
    },
    "#Analista": {
        "nome": "Analista",
        "descricao": "Avalia resultados, métricas e desempenho para gerar conclusões.",
        "instrucoes": (
            "Analise os resultados e métricas fornecidos. Identifique desvios, pontos fortes "
            "e fracos, e gere conclusões analíticas com recomendações de melhoria."
        ),
    },
}

# ==============================================================================
# MAPEAMENTO DOS PONTOS-CHAVE PARA APRESENTAÇÃO
# Relaciona cada Skill a um ponto-chave da apresentação estratégica ao cliente.
# ==============================================================================
PONTOS_CHAVE_APRESENTACAO = {
    "#Arquiteto": "DNA",
    "#Inteligência": "Mercado",
    "#Estrategista": "Editorial",
    "#Curador": "Identidade",
    "#Analista": "Performance",
}

# ==============================================================================
# FUNÇÃO PRINCIPAL: processar_com_ia
# Simula a chamada para cada Skill específica, gerando insights automáticos
# baseados nos dados inseridos pelo usuário e nas instruções da Skill.
# ==============================================================================
def processar_com_ia(skill_id: str, dados: dict) -> str:
    """
    Simula a chamada para uma Skill específica e gera insights automáticos.

    Parâmetros:
        skill_id (str): Identificador da Skill (ex.: '#Arquiteto').
        dados (dict): Dicionário com os dados inseridos pelo usuário.

    Retorno:
        str: Texto com os insights gerados pela simulação de IA.
    """
    skill = SKILLS.get(skill_id)
    if not skill:
        return "Skill não encontrada."

    # Consolida os dados não vazios em um resumo textual
    resumo_dados = "\n".join(
        f"- {chave.replace('_', ' ').title()}: {valor}"
        for chave, valor in dados.items()
        if valor
    ) or "- Nenhum dado inserido."

    # Simulação de geração de insights baseada nas instruções da Skill
    insights = (
        f"🤖 Insight gerado pela Skill {skill_id} ({skill['nome']}):\n\n"
        f"Instruções aplicadas: {skill['instrucoes']}\n\n"
        f"Dados analisados:\n{resumo_dados}\n\n"
        f"➡️ Recomendação automática: "
    )

    # Lógica simulada específica por Skill
    if skill_id == "#Arquiteto":
        insights += (
            "Estruture o projeto em pilares claros, garantindo alinhamento entre escopo e objetivos. "
            "Defina marcos de entrega e dependências críticas antes de avançar."
        )
    elif skill_id == "#Inteligência":
        insights += (
            "Mapeie as informações de mercado em categorias (tendências, riscos, oportunidades). "
            "Priorize dados com maior impacto decisório."
        )
    elif skill_id == "#Estrategista":
        insights += (
            "Estabeleça 3 estratégias prioritárias com métricas de sucesso mensuráveis. "
            "Organize o plano de ação em fases de curto, médio e longo prazo."
        )
    elif skill_id == "#Curador":
        insights += (
            "Agrupe os conteúdos por temas relevantes, eliminando redundâncias. "
            "Identifique lacunas de informação que precisam ser preenchidas."
        )
    elif skill_id == "#Analista":
        insights += (
            "Compare os resultados com as métricas esperadas, destacando desvios. "
            "Gere recomendações de melhoria contínua baseadas nos pontos fortes e fracos."
        )

    return insights


# ==============================================================================
# INICIALIZAÇÃO DO ESTADO DA SESSÃO
# Mantém os dados inseridos e os insights gerados ao longo da navegação.
# ==============================================================================
if "dados_modulos" not in st.session_state:
    st.session_state["dados_modulos"] = {
        "#Arquiteto": {},
        "#Inteligência": {},
        "#Estrategista": {},
        "#Curador": {},
        "#Analista": {},
    }

if "insights_ia" not in st.session_state:
    st.session_state["insights_ia"] = {
        "#Arquiteto": "",
        "#Inteligência": "",
        "#Estrategista": "",
        "#Curador": "",
        "#Analista": "",
    }

if "relatorio_gerado" not in st.session_state:
    st.session_state["relatorio_gerado"] = ""

if "apresentacao_gerada" not in st.session_state:
    st.session_state["apresentacao_gerada"] = ""


# ==============================================================================
# FUNÇÃO AUXILIAR: renderizar_modulo
# Renderiza um módulo completo com inputs, botão 'Processar com IA' e exibição
# dos insights gerados.
# ==============================================================================
def renderizar_modulo(skill_id: str, campos: list):
    """
    Renderiza um módulo da plataforma correspondente a uma Skill.

    Parâmetros:
        skill_id (str): Identificador da Skill.
        campos (list): Lista de tuplas (chave, rótulo, tipo) para os inputs.
    """
    skill = SKILLS[skill_id]
    st.header(f"{skill_id} — {skill['nome']}")
    st.caption(skill["descricao"])

    dados = {}
    with st.form(key=f"form_{skill_id}"):
        for chave, rotulo, tipo in campos:
            if tipo == "text":
                dados[chave] = st.text_input(rotulo, key=f"{skill_id}_{chave}")
            elif tipo == "textarea":
                dados[chave] = st.text_area(rotulo, height=120, key=f"{skill_id}_{chave}")
            elif tipo == "number":
                dados[chave] = st.number_input(rotulo, min_value=0.0, format="%.2f", key=f"{skill_id}_{chave}")
            elif tipo == "date":
                dados[chave] = str(st.date_input(rotulo, key=f"{skill_id}_{chave}"))
        submitted = st.form_submit_button("Salvar dados")
        if submitted:
            st.session_state["dados_modulos"][skill_id] = dados
            st.success(f"Dados do módulo {skill_id} salvos com sucesso!")

    # Botão 'Processar com IA' fora do formulário para permitir reprocessamento
    if st.button(f"Processar com IA — {skill_id}", key=f"btn_ia_{skill_id}"):
        dados_salvos = st.session_state["dados_modulos"][skill_id]
        if not any(dados_salvos.values()):
            st.warning("Insira e salve os dados antes de processar com IA.")
        else:
            with st.spinner(f"Processando com a Skill {skill_id}..."):
                insight = processar_com_ia(skill_id, dados_salvos)
                st.session_state["insights_ia"][skill_id] = insight
            st.success("Insights gerados com sucesso!")

    # Exibe os insights gerados pela IA, se existirem
    insight_atual = st.session_state["insights_ia"][skill_id]
    if insight_atual:
        st.subheader("Insights gerados pela IA")
        st.info(insight_atual)

    st.divider()


# ==============================================================================
# FUNÇÃO: gerar_relatorio_estrategico
# Consolida tanto os inputs manuais quanto os insights gerados pela IA em um
# relatório estratégico final.
# ==============================================================================
def gerar_relatorio_estrategico() -> str:
    """
    Gera o relatório estratégico final consolidando inputs manuais e insights de IA.

    Retorno:
        str: Texto formatado do relatório estratégico.
    """
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    linhas = [
        "=" * 70,
        "RELATÓRIO ESTRATÉGICO CONSOLIDADO",
        f"Data de geração: {data_atual}",
        "=" * 70,
        "",
    ]

    for skill_id, skill in SKILLS.items():
        linhas.append(f"▶ MÓDULO: {skill_id} — {skill['nome']}")
        linhas.append(f"   Descrição: {skill['descricao']}")
        linhas.append("")
        linhas.append("   📝 Inputs manuais:")
        dados = st.session_state["dados_modulos"].get(skill_id, {})
        if any(dados.values()):
            for chave, valor in dados.items():
                if valor:
                    rotulo = chave.replace("_", " ").title()
                    linhas.append(f"      - {rotulo}: {valor}")
        else:
            linhas.append("      - Nenhum input manual registrado.")
        linhas.append("")
        linhas.append("   🤖 Insights gerados pela IA:")
        insight = st.session_state["insights_ia"].get(skill_id, "")
        if insight:
            for linha_insight in insight.split("\n"):
                linhas.append(f"      {linha_insight}")
        else:
            linhas.append("      - Nenhum insight gerado para este módulo.")
        linhas.append("")
        linhas.append("-" * 70)
        linhas.append("")

    linhas.append("=" * 70)
    linhas.append("FIM DO RELATÓRIO ESTRATÉGICO")
    linhas.append("=" * 70)

    return "\n".join(linhas)


# ==============================================================================
# FUNÇÃO: gerar_apresentacao_estrategia
# Consolida os dados de todos os módulos em um resumo estruturado para
# apresentação de entrega ao cliente, organizado pelos pontos-chave:
# DNA, Mercado, Editorial, Identidade e Performance.
# ==============================================================================
def gerar_apresentacao_estrategia() -> str:
    """
    Gera um resumo estruturado para apresentação de entrega ao cliente,
    consolidando os dados de todos os módulos e organizando-os pelos
    pontos-chave: DNA, Mercado, Editorial, Identidade e Performance.

    Retorno:
        str: Texto formatado da apresentação de estratégia.
    """
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    linhas = [
        "=" * 70,
        "🎯 APRESENTAÇÃO DE ESTRATÉGIA — RESUMO PARA ENTREGA AO CLIENTE",
        f"Data de geração: {data_atual}",
        "=" * 70,
        "",
        "Esta apresentação consolida os pontos-chave de todos os módulos da",
        "Plataforma Estratégica com IA, organizando-os em 5 pilares fundamentais",
        "para uma comunicação clara e profissional ao cliente.",
        "",
        "─" * 70,
        "",
    ]

    for skill_id, ponto_chave in PONTOS_CHAVE_APRESENTACAO.items():
        skill = SKILLS[skill_id]
        dados = st.session_state["dados_modulos"].get(skill_id, {})
        insight = st.session_state["insights_ia"].get(skill_id, "")

        linhas.append(f"📌 PONTO-CHAVE: {ponto_chave.upper()}")
        linhas.append(f"   Skill de origem: {skill_id} — {skill['nome']}")
        linhas.append(f"   {skill['descricao']}")
        linhas.append("")

        # Resumo dos inputs manuais relevantes
        linhas.append("   📝 Dados consolidados:")
        if any(dados.values()):
            for chave, valor in dados.items():
                if valor:
                    rotulo = chave.replace("_", " ").title()
                    linhas.append(f"      • {rotulo}: {valor}")
        else:
            linhas.append("      • Nenhum dado inserido neste pilar.")
        linhas.append("")

        # Recomendação estratégica extraída dos insights de IA
        linhas.append("   🤖 Recomendação estratégica:")
        if insight:
            # Extrai a recomendação automática (após "➡️ Recomendação automática: ")
            if "➡️ Recomendação automática:" in insight:
                recomendacao = insight.split("➡️ Recomendação automática:")[-1].strip()
                linhas.append(f"      {recomendacao}")
            else:
                linhas.append(f"      {insight}")
        else:
            linhas.append("      • Nenhuma recomendação gerada para este pilar.")
        linhas.append("")
        linhas.append("─" * 70)
        linhas.append("")

    # Síntese final para o cliente
    linhas.append("📊 SÍNTESE EXECUTIVA PARA O CLIENTE")
    linhas.append("")
    linhas.append("Esta apresentação reúne os 5 pilares estratégicos do projeto:")
    linhas.append("   1. DNA — Fundação, escopo e objetivos do projeto.")
    linhas.append("   2. Mercado — Contexto, concorrência e tendências identificadas.")
    linhas.append("   3. Editorial — Estratégias, prioridades e plano de ação.")
    linhas.append("   4. Identidade — Curadoria de conteúdos, temas e recursos.")
    linhas.append("   5. Performance — Resultados, métricas e recomendações de melhoria.")
    linhas.append("")
    linhas.append("Utilize este resumo como roteiro para a apresentação profissional")
    linhas.append("de entrega ao cliente, garantindo clareza e alinhamento estratégico.")
    linhas.append("")
    linhas.append("=" * 70)
    linhas.append("FIM DA APRESENTAÇÃO DE ESTRATÉGIA")
    linhas.append("=" * 70)

    return "\n".join(linhas)


# ==============================================================================
# BARRA LATERAL — NAVEGAÇÃO ENTRE MÓDULOS
# ==============================================================================
st.sidebar.title("🧠 Plataforma Estratégica com IA")
st.sidebar.markdown("Navegue entre os módulos das 5 Skills:")

modulos = [
    ("#Arquiteto", "🏗️ Arquiteto"),
    ("#Inteligência", "🔍 Inteligência"),
    ("#Estrategista", "♟️ Estrategista"),
    ("#Curador", "📚 Curador"),
    ("#Analista", "📊 Analista"),
    ("#Relatorio", "📋 Relatório Estratégico"),
]

opcao = st.sidebar.radio("Selecione um módulo:", options=modulos, format_func=lambda x: x[1])
modulo_selecionado = opcao[0]

# ==============================================================================
# RENDERIZAÇÃO DOS MÓDULOS
# ==============================================================================
st.title("Plataforma Estratégica com IA")
st.markdown(
    "Esta plataforma integra 5 Skills especializadas para apoiar a construção "
    "de projetos estratégicos. Cada módulo permite inserir dados manuais e "
    "gerar insights automáticos por meio da função `processar_com_ia`."
)

if modulo_selecionado == "#Arquiteto":
    renderizar_modulo(
        "#Arquiteto",
        [
            ("nome_projeto", "Nome do Projeto", "text"),
            ("escopo", "Escopo do Projeto", "textarea"),
            ("objetivos", "Objetivos Principais", "textarea"),
            ("data_inicio", "Data de Início", "date"),
        ],
    )

elif modulo_selecionado == "#Inteligência":
    renderizar_modulo(
        "#Inteligência",
        [
            ("contexto", "Contexto Atual", "textarea"),
            ("mercado", "Análise de Mercado", "textarea"),
            ("concorrentes", "Principais Concorrentes", "text"),
            ("tendencias", "Tendências Identificadas", "textarea"),
        ],
    )

elif modulo_selecionado == "#Estrategista":
    renderizar_modulo(
        "#Estrategista",
        [
            ("estrategias", "Estratégias Propostas", "textarea"),
            ("prioridades", "Prioridades", "textarea"),
            ("metricas", "Métricas de Sucesso", "textarea"),
            ("prazo", "Prazo Estimado (meses)", "number"),
        ],
    )

elif modulo_selecionado == "#Curador":
    renderizar_modulo(
        "#Curador",
        [
            ("conteudos", "Conteúdos Selecionados", "textarea"),
            ("recursos", "Recursos Relevantes", "textarea"),
            ("temas", "Temas Organizados", "text"),
            ("lacunas", "Lacunas Identificadas", "textarea"),
        ],
    )

elif modulo_selecionado == "#Analista":
    renderizar_modulo(
        "#Analista",
        [
            ("resultados", "Resultados Obtidos", "textarea"),
            ("metricas_avaliadas", "Métricas Avaliadas", "textarea"),
            ("desvios", "Desvios Identificados", "textarea"),
            ("recomendacoes", "Recomendações de Melhoria", "textarea"),
        ],
    )

elif modulo_selecionado == "#Relatorio":
    st.header("📋 Relatório Estratégico Consolidado")
    st.caption(
        "Consolida tanto os inputs manuais quanto os insights gerados pela IA "
        "em todos os módulos."
    )

    # Verifica se há dados ou insights em pelo menos um módulo
    tem_dados = any(
        any(dados.values())
        for dados in st.session_state["dados_modulos"].values()
    )
    tem_insights = any(
        bool(insight)
        for insight in st.session_state["insights_ia"].values()
    )

    if not tem_dados and not tem_insights:
        st.warning(
            "Nenhum dado ou insight encontrado. Preencha os módulos e processe "
            "com IA antes de gerar o relatório."
        )
    else:
        if st.button("Gerar Relatório Estratégico", key="btn_relatorio"):
            with st.spinner("Consolidando dados e insights..."):
                relatorio = gerar_relatorio_estrategico()
                st.session_state["relatorio_gerado"] = relatorio
            st.success("Relatório estratégico gerado com sucesso!")

        relatorio = st.session_state.get("relatorio_gerado", "")
        if relatorio:
            st.subheader("Relatório Gerado")
            st.text_area(
                "Conteúdo do Relatório",
                value=relatorio,
                height=400,
                key="area_relatorio",
            )

            # Permite baixar o relatório em formato texto
            st.download_button(
                label="⬇️ Baixar Relatório (.txt)",
                data=relatorio.encode("utf-8"),
                file_name="relatorio_estrategico.txt",
                mime="text/plain",
            )

            # Permite baixar os dados consolidados em formato JSON
            dados_consolidados = {
                "data_geracao": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "dados_modulos": st.session_state["dados_modulos"],
                "insights_ia": st.session_state["insights_ia"],
            }
            st.download_button(
                label="⬇️ Baixar Dados Consolidados (.json)",
                data=json.dumps(dados_consolidados, ensure_ascii=False, indent=2).encode("utf-8"),
                file_name="dados_consolidados.json",
                mime="application/json",
            )

        st.divider()

        # ------------------------------------------------------------------
        # SEÇÃO: APRESENTAÇÃO DE ESTRATÉGIA
        # ------------------------------------------------------------------
        st.subheader("🎯 Apresentação de Estratégia")
        st.info(
            "Ao clicar no botão **'Gerar Apresentação de Estratégia'**, o sistema "
            "consolida os dados de todos os módulos e organiza os pontos-chave "
            "(**DNA**, **Mercado**, **Editorial**, **Identidade** e **Performance**) "
            "em um resumo estruturado, pronto para uma apresentação profissional "
            "de entrega ao cliente."
        )

        if st.button("Gerar Apresentação de Estratégia", key="btn_apresentacao"):
            with st.spinner("Organizando pontos-chave para a apresentação..."):
                apresentacao = gerar_apresentacao_estrategia()
                st.session_state["apresentacao_gerada"] = apresentacao
            st.success("Apresentação de estratégia gerada com sucesso!")

        apresentacao = st.session_state.get("apresentacao_gerada", "")
        if apresentacao:
            st.text_area(
                "Conteúdo da Apresentação",
                value=apresentacao,
                height=400,
                key="area_apresentacao",
            )

            # Permite baixar a apresentação em formato texto
            st.download_button(
                label="⬇️ Baixar Apresentação (.txt)",
                data=apresentacao.encode("utf-8"),
                file_name="apresentacao_estrategia.txt",
                mime="text/plain",
            )