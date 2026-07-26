import streamlit as st
import json
import random
import time
from datetime import datetime

# --- CONFIGURAÇÕES E DADOS PADRÃO ---
DIAS_SEMANA_PT = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

# Falas icônicas do anime Solo Leveling para o Level Up
FRASES_LEVEL_UP = [
    "O Sistema determinou que você é digno de mais poder. Erga-se (Arise)!",
    "Se eu ficar mais forte, tudo o que eu perdi... eu poderei recuperar?",
    "Não importa o quão desesperadora a situação pareça, sempre há um caminho para vencer.",
    "O Sistema me escolheu por um motivo. Eu continuarei subindo, não importa o preço.",
    "Aqueles que zombavam do caçador mais fraco do mundo sumirão na sua sombra.",
    "Eu sou o único que consegue subir de nível neste mundo. Avance!"
]

MAPA_ATRIBUTOS = {
    "💪 Força": "Força",
    "📚 Inteligência": "Inteligência",
    "💧 Vitalidade": "Vitalidade",
    "👥 Carisma": "Carisma",
    "⚡ Agilidade": "Agilidade"
}

# Loja expandida com mais itens divertidos de recompensa
LOJA_SISTEMA = {
    "1": {"nome": "🧪 Poção de Mana (Ver 1 episódio de anime/série)", "custo": 50},
    "2": {"nome": "📜 Pergaminho de Retorno (Fim de semana livre de videogame)", "custo": 200},
    "3": {"nome": "🍖 Elixir da Juventude (Uma refeição livre/Lanche)", "custo": 300},
    "4": {"nome": "🔑 Chave de Dungeon (Comprar um mimo ou livro novo)", "custo": 500},
    "5": {"nome": "🗡️ Adaga do Rei Demônio (Direito a ignorar 1 tarefa obrigatória sem punição)", "custo": 600},
    "6": {"nome": "👑 Coroa do Monarca (Dia inteiro de descanso absoluto/Ócio sagrado)", "custo": 1000}
}

progresso_padrao = {
    "nome": "Sung Jin-Woo", 
    "nivel": 1, 
    "xp": 0, 
    "ouro": 0,
    "atributos": {"Força": 10, "Inteligência": 10, "Vitalidade": 10, "Carisma": 10, "Agilidade": 10},
    "missoes": [
        {"id": 1, "nome": "💪 100 Flexões / Treino Físico", "xp": 100, "ouro": 50, "attr": "Força", "dias": ["Segunda", "Quarta", "Sexta"], "recorrente": True, "concluida_em": ""},
        {"id": 2, "nome": "📚 Estudar Python / Foco", "xp": 150, "ouro": 75, "attr": "Inteligência", "dias": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"], "recorrente": True, "concluida_em": ""},
        {"id": 3, "nome": "👥 Tempo de Qualidade com a Família", "xp": 80, "ouro": 40, "attr": "Carisma", "dias": ["Sábado", "Domingo"], "recorrente": True, "concluida_em": ""}
    ],
    "inventario": {}
}

def calcular_xp_nec(nivel):
    if nivel == 1:
        return 100
    return int(100 * (nivel ** 1.8))

# Tabela automática de Ranks de Caçador baseada no nível do jogador
def obter_rank_cacador(nivel):
    if nivel >= 80: return "👑 Monarca Sombra (Rank S+)"
    elif nivel >= 60: return "⚔️ Caçador Rank S"
    elif nivel >= 45: return "🛡️ Caçador Rank A"
    elif nivel >= 30: return "🏹 Caçador Rank B"
    elif nivel >= 15: return "🗡️ Caçador Rank C"
    elif nivel >= 5: return "🪓 Caçador Rank D"
    return "🦴 Caçador Rank E (O Mais Fraco do Mundo)"

def obter_dia_atual_pt():
    indice = datetime.now().weekday()
    return DIAS_SEMANA_PT[indice]

if "dados_jogador" not in st.session_state:
    st.session_state["dados_jogador"] = json.loads(json.dumps(progresso_padrao))

dados = st.session_state["dados_jogador"]
data_hoje = datetime.now().strftime("%Y-%m-%d")
dia_hoje_nome = obter_dia_atual_pt()

# Ciclo automático de renovação diária de tarefas
for m_ciclo in dados["missoes"]:
    if m_ciclo["concluida_em"] != "" and m_ciclo["concluida_em"] != data_hoje:
        if m_ciclo.get("recorrente", True):
            m_ciclo["concluida_em"] = ""

st.set_page_config(page_title="Solo Leveling", page_icon="⚡", layout="centered")

# --- CONTROLADOR CENTRAL DE NAVEGAÇÃO MOBILE (SIDEBAR) ---
st.sidebar.title("🎮 MENU DO SISTEMA")
opcao_menu = st.sidebar.radio(
    "Navegue pelas seções:",
    ["👤 Meu Status", "🎯 Missões de Hoje", "🛒 Loja e Mochila", "➕ Adicionar Hábito", "❌ Configurações Críticas"]
)

# --- SEÇÃO 1: STATUS ---
if opcao_menu == "👤 Meu Status":
    st.header("👤 PERFIL DO CAÇADOR")
    st.subheader(f"Nome: {dados['nome']}")
    
    # Exibe o Rank atual obtido automaticamente pelas conquistas de nível
    st.info(f"🏆 **Rank Atual:** {obter_rank_cacador(dados['nivel'])}")
    
    with st.expander("⚙️ Alterar Nome"):
        novo_nome_input = st.text_input("Novo nome:", value=dados["nome"])
        if st.button("Confirmar Despertar"):
            if novo_nome_input.strip():
                dados["nome"] = novo_nome_input.strip()
                st.rerun()

    xp_nec = calcular_xp_nec(dados["nivel"])
    st.progress(min(dados["xp"] / xp_nec, 1.0), text=f"Nível {dados['nivel']} ({dados['xp']}/{xp_nec} XP)")
    
    st.write(f"**💰 Ouro:** {dados['ouro']} moedas")
    st.write(f"**📅 Calendário:** {dia_hoje_nome}-feira")
    
    st.write("### 📊 Status de Atributos")
    for attr, valor in dados["atributos"].items():
        st.write(f"• **{attr}:** {valor}")

# --- SEÇÃO 2: MISSÕES DE HOJE ---
elif opcao_menu == "🎯 Missões de Hoje":
    st.header(f"🎯 META DIÁRIA ({dia_hoje_nome}-feira)")
    missoes_hoje = [m for m in dados["missoes"] if dia_hoje_nome in m.get("dias", [])]
    
    if not missoes_hoje:
        st.info("⚔️ Nenhuma obrigação agendada para hoje! Use o tempo para descansar.")
    else:
        for m in missoes_hoje:
            foi_concluida = m["concluida_em"] == data_hoje
            st.write(f"#### {m['nome']}")
            st.caption(f"Recompensa: +{m['xp']} XP | +💰{m['ouro']} | Evolui: {m['attr']}")
            
            if foi_concluida:
                st.success("✅ Objetivo Cumprido Hoje!")
            else:
                col_btn_1, col_btn_2 = st.columns(2)
                
                if col_btn_1.button("Concluir Objetivo", key=f"btn_done_{m['id']}"):
                    m["concluida_em"] = data_hoje
                    dados["xp"] += m["xp"]
                    dados["ouro"] += m["ouro"]
                    dados["atributos"][m["attr"]] += 1
                    
                    if not m.get("recorrente", True):
                        dados["missoes"].remove(m)
                        
                    while dados["xp"] >= calcular_xp_nec(dados["nivel"]):
                        dados["xp"] -= calcular_xp_nec(dados["nivel"])
                        dados["nivel"] += 1
                        st.balloons()
                        st.success(f"🎉 LEVEL UP NÍVEL {dados['nivel']}!\n_{random.choice(FRASES_LEVEL_UP)}_")
                    time.sleep(1)
                    st.rerun()
                
                if col_btn_2.button("🚨 Falhar Meta", key=f"btn_fail_{m['id']}"):
                    dados["xp"] = max(0, dados["xp"] - m["xp"])
                    dados["ouro"] = max(0, dados["ouro"] - m["ouro"])
                    dados["atributos"][m["attr"]] = max(10, dados["atributos"][m["attr"]] - 1)
                    st.sidebar.error(f"Punição aplicada! -{m['xp']} XP | -💰{m['ouro']}")
                    time.sleep(1)
                    st.rerun()
            st.write("---")

# --- SEÇÃO 3: LOJA E INVENTÁRIO ---
elif opcao_menu == "🛒 Loja e Mochila":
    st.header("🛒 LOJA DO SISTEMA")
    st.subheader(f"Seu Saldo: 💰 {dados['ouro']} Ouro")
    
    for k, item in LOJA_SISTEMA.items():
        st.write(f"**{item['nome']}**")
        st.caption(f"Custo: 💰 {item['custo']} Ouro")
        if st.button("Comprar Recompensa", key=f"buy_m_{k}"):
            if dados["ouro"] >= item["custo"]:
                dados["ouro"] -= item["custo"]
                dados["inventario"][item["nome"]] = dados["inventario"].get(item["nome"], 0) + 1
                st.toast("🛒 Adquirido!")
                st.rerun()
            else:
                st.error("Ouro insuficiente!")
        st.write("---")
        
    st.header("🎒 SUA MOCHILA (VOUCHERS)")
    if not dados["inventario"]:
        st.caption("Inventário vazio.")
    else:
        for nome_item, qtd in list(dados["inventario"].items()):
            st.write(f"• **{nome_item}** (Quantidade: x{qtd})")
            if st.button("Gastar Recompensa", key=f"use_m_{nome_item}"):
                dados["inventario"][nome_item] -= 1
                if dados["inventario"][nome_item] <= 0:
                    del dados["inventario"][nome_item]
                st.balloons()
                st.rerun()

# --- SEÇÃO 4: ADICIONAR HÁBITO ---
elif opcao_menu == "➕ Adicionar Hábito":
    st.header("➕ NOVO OBJETIVO")
    
    novo_name = st.text_input("Nome do hábito/rotina:")
    attr_sel = st.selectbox("Qual atributo ele vai treinar?", list(MAPA_ATRIBUTOS.keys()))
    dias_sel = st.multiselect("Em quais dias ele deve surgir?", options=DIAS_SEMANA_PT, default=[dia_hoje_nome])
    
    recorrencia_tipo = st.radio("Frequência:", ("🔄 Recorrente (Toda semana)", "📌 Única (Executa e some)"))
    is_recorrente = True if "Recorrente" in recorrencia_tipo else False
    
    rxp = st.number_input("Recompensa de XP:", min_value=10, max_value=1000, value=100, step=10)
    rouro = st.number_input("Recompensa de Ouro:", min_value=5, max_value=500, value=50, step=5)
    
    if st.button("Sincronizar com o Sistema"):
        if not novo_name or not dias_sel:
            st.error("Preencha o nome e selecione pelo menos um dia da semana!")
        else:
            nid = int(time.time() * 1000) + random.randint(1, 99)
            nova_missao = {"id": nid, "nome": novo_name, "xp": int(rxp), "ouro": int(rouro), "attr": MAPA_ATRIBUTOS[attr_sel], "dias": dias_sel, "recorrente": is_recorrente, "concluida_em": ""}
            dados["missoes"].append(nova_missao)
            st.success("Hábito agendado com sucesso!")
            time.sleep(1)
            st.rerun()

# --- SEÇÃO 5: CONFIGURAÇÕES CRÍTICAS ---
elif opcao_menu == "❌ Configurações Críticas":
    st.header("❌ REMOVER MISSÕES")
    
    if not dados["missoes"]:
        st.caption("Nenhum hábito cadastrado para deletar.")
    else:
        for idx, m in enumerate(dados["missoes"]):
