# app.py - Sistema de Avaliação de Skills com Autenticação Simples (Streamlit)

import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# =============================================================================
# CONFIGURAÇÃO DE CREDENCIAIS DE LOGIN
# -----------------------------------------------------------------------------
# Para alterar o usuário e senha padrão, modifique as variáveis abaixo.
# Exemplo: VALID_USER = "joao" e VALID_PASSWORD = "minhaSenha123"
# Recomenda-se, em produção, usar variáveis de ambiente ou um gerenciador
# seguro de segredos em vez de hardcoded no código.
# =============================================================================
VALID_USER = "admin"
VALID_PASSWORD = "admin"


def check_password():
    """Exibe o formulário de login e retorna True apenas se as credenciais forem válicas."""
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
# Layout principal
# -----------------------------------------------------------------------------
st.title("📊 Sistema de Avaliação de Skills")
st.sidebar.title("Navegação")
opcao = st.sidebar.radio("Selecione uma seção:", ["Apresentação", "Skills", "Relatórios"])

if opcao == "Apresentação":
    st.header("📌 Apresentação")
    st.write(
        "Bem-vindo ao Sistema de Avaliação de Skills! "
        "Este aplicativo permite cadastrar, visualizar e gerar relatórios "
        "das competências da equipe, além de obter sugestões de desenvolvimento "
        "por meio de botões de IA."
    )
    st.write("Use o menu lateral para navegar entre as seções.")

elif opcao == "Skills":
    st.header("🧠 Skills")
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
            if st.button(f"Sugestão IA", key=f"ia_{row['Skill']}"):
                st.info(sugestao_ia(row["Skill"], row["Nível"]))

elif opcao == "Relatórios":
    st.header("📄 Relatórios")
    df = carregar_skills()

    st.subheader("Relatório de Skills")
    relatorio = gerar_relatorio_skills(df)
    st.text(relatorio)

    st.subheader("Exportar Relatório")
    st.download_button(
        label="⬇️ Baixar relatório (.txt)",
        data=relatorio,
        file_name=f"relatorio_skills_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
    )

    st.subheader("Exportar dados (.csv)")
    st.download_button(
        label="⬇️ Baixar dados (.csv)",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=f"skills_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
    )
