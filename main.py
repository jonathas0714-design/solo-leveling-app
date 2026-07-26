import streamlit as st
import json
import random
import time
from datetime import datetime

# --- CONFIGURAÇÕES E DADOS PADRÃO ---
DIAS_SEMANA_PT = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

FRASES_LEVEL_UP = [
    "O Sistema determinou que você é digno de mais poder. Continue erguendo-se!",
    "Do Caçador mais fraco do mundo ao topo absoluto. O despertar continua!",
    "O medo é apenas uma ilusão. Você acabou de quebrar mais um limite!",
    "O Sistema reconhece sua evolução. Erga-se (Arise)!"
]

MAPA_ATRIBUTOS = {
    "💪 Força": "Força",
    "📚 Inteligência": "Inteligência",
    "💧 Vitalidade": "Vitalidade",
    "👥 Carisma": "Carisma",
    "⚡ Agilidade": "Agilidade"
}

LOJA_SISTEMA = {
    "1": {"nome": "🧪 Poção de Mana (Ver 1 episódio de anime/série)", "custo": 50},
    "2": {"nome": "📜 Pergaminho de Retorno (Fim de semana livre de videogame)", "custo": 200},
    "3": {"nome": "🍖 Elixir da Juventude (Uma refeição livre/Lanche)", "custo": 300},
    "4": {"nome": "🔑 Chave de Dungeon (Comprar um mimo ou livro novo)", "custo": 500}
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

def obter_dia_atual_pt():
    indice = datetime.now().weekday()
    return DIAS_SEMANA_PT[indice]

def gerenciar_ciclo_de_datas(dados, data_hoje):
    nova_lista_missoes = []
    mudou = False
    for m in dados["missoes"]:
        if not m.get("recorrente", True) and m["concluida_em"] != "" and m["concluida_em"] != data_hoje:
            mudou = True
            continue
        if m.get("recorrente", True) and m["concluida_em"] != "" and m["concluida_em"] != data_hoje:
            m["concluida_em"] = ""
            mudou = True
        nova_lista_missoes.append(m)
    if mudou:
        dados["missoes"] = nova_lista_missoes

# --- CALLBACKS DO SISTEMA (AÇÕES EM SEGUNDO PLANO) ---
def callback_deletar(missao_alvo):
    st.session_state["dados_jogador"]["missoes"].remove(missao_alvo)
    st.toast("❌ Missão removida do Sistema!")

def callback_falhar(missao_alvo):
    dados = st.session_state["dados_jogador"]
    dados["xp"] = max(0, dados["xp"] - missao_alvo["xp"])
    dados["ouro"] = max(0, dados["ouro"] - missao_alvo["ouro"])
    dados["atributos"][missao_alvo["attr"]] = max(10, dados["atributos"][missao_alvo["attr"]] - 1)
    st.sidebar.error(f"🚨 PENALIDADE: Perdeu XP, Ouro e -1 em {missao_alvo['attr']}!")

def callback_resetar():
    st.session_state["dados_jogador"]["nivel"] = 1
    st.session_state["dados_jogador"]["xp"] = 0
    st.session_state["dados_jogador"]["ouro"] = 0
    st.session_state["dados_jogador"]["atributos"] = {"Força": 10, "Inteligência": 10, "Vitalidade": 10, "Carisma": 10, "Agilidade": 10}
    st.session_state["dados_jogador"]["inventario"] = {}
    st.sidebar.warning("💥 O Sistema foi completamente resetado!")

# --- CONFIGURAÇÃO DA TELA MÓVEL ---
st.set_page_config(page_title="Solo Leveling System", page_icon="⚡", layout="centered")
st.title("⚡ SOLO LEVELING SYSTEM")

if "dados_jogador" not in st.session_state:
    st.session_state["dados_jogador"] = json.loads(json.dumps(progresso_padrao))

dados = st.session_state["dados_jogador"]
data_hoje = datetime.now().strftime("%Y-%m-%d")
dia_hoje_nome = obter_dia_atual_pt()

gerenciar_ciclo_de_datas(dados, data_hoje)

aba_status, aba_missoes, aba_loja, aba_cadastrar, aba_excluir = st.tabs([
    "👤 Status", "🎯 Missões de Hoje", "🛒 Loja", "➕ Criar Hábito", "❌ Configurações Críticas"
])

# --- 1. ABA STATUS ---
with aba_status:
    st.subheader(f"Caçador: {dados['nome']}")
    with st.expander("⚙️ Alterar Nome do Caçador"):
        novo_nome_input = st.text_input("Insira seu nome ou apelido:", value=dados["nome"])
        if st.button("Confirmar Despertar"):
            if novo_nome_input.strip():
                dados["nome"] = novo_nome_input.strip()
                st.rerun()

    xp_nec = calcular_xp_nec(dados["nivel"])
    progresso_barra = min(dados["xp"] / xp_nec, 1.0)
    st.progress(progresso_barra, text=f"Nível {dados['nivel']} ({dados['xp']}/{xp_nec} XP)")
    
    col1, col2 = st.columns(2)
    col1.metric("💰 Ouro", f"{dados['ouro']}")
    col2.metric("📅 Hoje", f"{dia_hoje_nome}-feira")
    
    st.write("### 📊 Status de Atributos")
    for attr, valor in dados["atributos"].items():
        st.write(f"**{attr}:** {valor}")

# --- 2. ABA MISSÕES ---
with aba_missoes:
    st.write(f"### Objetivos Disponíveis para Hoje")
    missoes_hoje = [m for m in dados["missoes"] if dia_hoje_nome in m.get("dias", [])]
    
    if not missoes_hoje:
        st.info("⚔️ Nenhuma missão agendada para hoje! Descanse.")
    else:
        for m in missoes_hoje:
            foi_concluida = m["concluida_em"] == data_hoje
            tipo_txt = "🔄 Recorrente" if m.get("recorrente", True) else "📌 Única"
            
            col_task, col_fail = st.columns([3, 1])
            with col_task:
                check = st.checkbox(f"{m['nome']} (+{m['xp']}XP | +💰{m['ouro']}) [{tipo_txt}]", value=foi_concluida, key=f"m_{m['id']}")
            with col_fail:
                # CORREÇÃO: Função de falha agora usa callback direto de clique estável
                st.button("🚨 Falhar", key=f"fail_{m['id']}", disabled=foi_concluida, on_click=callback_falhar, args=(m,))
                
            if check and not foi_concluida:
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
                    st.success(f"🎉 LEVEL UP NÍVEL {dados['nivel']}!\n{random.choice(FRASES_LEVEL_UP)}")
                st.rerun()
            elif not check and foi_concluida:
                m["concluida_em"] = ""
                dados["xp"] = max(0, dados["xp"] - m["xp"])
                dados["ouro"] = max(0, dados["ouro"] - m["ouro"])
                dados["atributos"][m["attr"]] = max(10, dados["atributos"][m["attr"]] - 1)
                st.rerun()

# --- 3. ABA LOJA ---
with aba_loja:
    st.write(f"### 👛 Saldo da Carteira: **{dados['ouro']} Ouro**")
    for k, item in LOJA_SISTEMA.items():
        col_item_info, col_item_botao = st.columns(2)
        col_item_info.write(f"**{item['nome']}**  \n_Custo: 💰 {item['custo']}_")
        if col_item_botao.button("Comprar", key=f"buy_{k}"):
            if dados["ouro"] >= item["custo"]:
                dados["ouro"] -= item["custo"]
                dados["inventario"][item["nome"]] = dados["inventario"].get(item["nome"], 0) + 1
                st.toast("🛒 Item adquirido!")
                st.rerun()
            else: st.error("Ouro insuficiente!")

    st.write("---")
    st.write("### 🎒 Seu Inventário")
    for nome_item, qtd in list(dados["inventario"].items()):
        col_inv_info, col_inv_botao = st.columns(2)
        col_inv_info.write(f"• **{nome_item}** (x{qtd})")
        if col_inv_botao.button("Usar", key=f"use_{nome_item}"):
            dados["inventario"][nome_item] -= 1
            if dados["inventario"][nome_item] <= 0: del dados["inventario"][nome_item]
            st.balloons()
            st.rerun()

# --- 4. ABA CRIAR HÁBITO ---
with aba_cadastrar:
    st.write("### ➕ Cadastrar Novo Objetivo")
    with st.form("formulario_habito", clear_on_submit=True):
        novo_name = st.text_input("Nome do hábito:")
        attr_sel = st.selectbox("Atributo de Treino:", list(MAPA_ATRIBUTOS.keys()))
        dias_sel = st.multiselect("Dias da semana:", options=DIAS_SEMANA_PT, default=[dia_hoje_nome])
        recorrencia_tipo = st.radio("Repetição:", ("🔄 Recorrente", "📌 Única"))
        is_recorrente = True if "Recorrente" in recorrencia_tipo else False
        rxp = st.number_input("XP", min_value=10, max_value=1000, value=100)
        rouro = st.number_input("Ouro", min_value=5, max_value=500, value=50)
        botao_salvar = st.form_submit_button("Salvar no Sistema")
        
        if botao_salvar and novo_name:
            if not dias_sel: st.error("Selecione um dia!")
            else:
                nid = int(time.time() * 1000) + random.randint(1, 99)
                nova_missao = {"id": nid, "nome": novo_name, "xp": int(rxp), "ouro": int(rouro), "attr": MAPA_ATRIBUTOS[attr_sel], "dias": dias_sel, "recorrente": is_recorrente, "concluida_em": ""}
                dados["missoes"].append(nova_missao)
                st.success("Hábito salvo!")
                st.rerun()

# --- 5. ABA CONFIGURAÇÕES CRÍTICAS (EXCLUSÃO E RESET BLINDADOS) ---
with aba_excluir:
    st.write("### ❌ Remover Missões Existentes")
    if not dados["missoes"]:
        st.caption("Nenhum hábito registrado.")
    else:
        for idx, m in enumerate(dados["missoes"]):
            col_info, col_botao = st.columns([3, 1])
            agenda_str = ", ".join([d[:3] for d in m.get("dias", [])])
