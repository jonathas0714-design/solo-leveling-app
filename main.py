import streamlit as st
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

# --- FUNÇÕES DE LOGICA E CURVA DE NÍVEL ---
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

# --- INTERFACE DO USUÁRIO (STREAMLIT) ---
st.set_page_config(page_title="Solo Leveling System", page_icon="⚡", layout="centered")
st.title("⚡ SOLO LEVELING SYSTEM")

# Armazenamento persistente em cache do navegador para não perder o save
if "dados_jogador" not in st.session_state:
    st.session_state["dados_jogador"] = progresso_padrao.copy()

dados = st.session_state["dados_jogador"]
data_hoje = datetime.now().strftime("%Y-%m-%d")
dia_hoje_nome = obter_dia_atual_pt()

gerenciar_ciclo_de_datas(dados, data_hoje)

aba_status, aba_missoes, aba_loja, aba_gerenciar_habitos = st.tabs([
    "👤 Status", 
    "🎯 Missões de Hoje", 
    "🛒 Loja do Sistema", 
    "🛠️ Gerenciar Hábitos"
])

# --- 1. ABA STATUS ---
with aba_status:
    st.subheader(f"Caçador: {dados['nome']}")
    
    with st.expander("⚙️ Alterar Nome do Caçador"):
        novo_nome_input = st.text_input("Insira seu nome ou apelido:", value=dados["nome"])
        if st.button("Confirmar Despertar"):
            if novo_nome_input.strip():
                dados["nome"] = novo_nome_input.strip()
                st.success("Identidade atualizada!")
                st.rerun()

    xp_nec = calcular_xp_nec(dados["nivel"])
    progresso_barra = min(dados["xp"] / xp_nec, 1.0)
    st.progress(progresso_barra, text=f"Nível {dados['nivel']} ({dados['xp']}/{xp_nec} XP)")
    
    col1, col2 = st.columns(2)
    col1.metric("💰 Ouro Acumulado", f"{dados['ouro']} Ouro")
    col2.metric("📅 Dia da Semana", f"{dia_hoje_nome}-feira")
    
    st.write("### 📊 Status de Atributos")
    for attr, valor in dados["atributos"].items():
        st.write(f"**{attr}:** {valor}")

# --- 2. ABA MISSÕES ---
with aba_missoes:
    st.write(f"### Objetivos Disponíveis para Hoje ({dia_hoje_nome}-feira)")
    missoes_hoje = [m for m in dados["missoes"] if dia_hoje_nome in m.get("dias", [])]
    
    if not missoes_hoje:
        st.info("⚔️ Nenhuma missão agendada para hoje! Use o dia para descansar e recuperar energias.")
    else:
        for m in missoes_hoje:
            foi_concluida = m["concluida_em"] == data_hoje
            tipo_txt = "🔄 Recorrente" if m.get("recorrente", True) else "📌 Única"
            
            col_task, col_fail = st.columns(2)
            
            with col_task:
                check = st.checkbox(f"{m['nome']} (+{m['xp']}XP | +💰{m['ouro']}) [{tipo_txt}]", value=foi_concluida, key=f"m_{m['id']}")
            
            with col_fail:
                botao_falha = st.button("🚨 Falhar", key=f"fail_{m['id']}", disabled=foi_concluida)
                
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
                    st.success(f"🎉 LEVEL UP! Nível {dados['nivel']}!\n{random.choice(FRASES_LEVEL_UP)}")
                st.rerun()
                
            elif not check and foi_concluida:
                m["concluida_em"] = ""
                dados["xp"] = max(0, dados["xp"] - m["xp"])
                dados["ouro"] = max(0, dados["ouro"] - m["ouro"])
                dados["atributos"][m["attr"]] = max(10, dados["atributos"][m["attr"]] - 1)
                st.rerun()
                
            if botao_falha:
                dados["xp"] = max(0, dados["xp"] - m["xp"])
                dados["ouro"] = max(0, dados["ouro"] - m["ouro"])
                dados["atributos"][m["attr"]] = max(10, dados["atributos"][m["attr"]] - 1)
                st.error(f"🚨 PENALIDADE DO SISTEMA! Você perdeu -{m['xp']} XP e -💰 {m['ouro']} Ouro.")
                time.sleep(1.5)
                st.rerun()

# --- 3. ABA LOJA E INVENTÁRIO ---
with aba_loja:
    st.write(f"### 👛 Saldo da Carteira: **{dados['ouro']} Ouro**")
    st.write("---")
    
    st.write("### 🛍️ Recompensas Disponíveis para Compra")
    for k, item in LOJA_SISTEMA.items():
        col_item_info, col_item_botao = st.columns(2)
        col_item_info.write(f"**{item['nome']}**  \n_Custo: 💰 {item['custo']} Ouro_")
        
        if col_item_botao.button("Comprar", key=f"buy_{k}"):
            if dados["ouro"] >= item["custo"]:
                dados["ouro"] -= item["custo"]
                dados["inventario"][item["nome"]] = dados["inventario"].get(item["nome"], 0) + 1
                st.toast(f"🛒 Adquirido: {item['nome']}!")
                st.rerun()
            else:
                st.error("🚨 Ouro insuficiente!")

    st.write("---")
    st.write("### 🎒 Seu Inventário")
    if not dados["inventario"]:
        st.caption("Seu inventário está vazio.")
    else:
        for nome_item, qtd in list(dados["inventario"].items()):
            col_inv_info, col_inv_botao = st.columns(2)
            col_inv_info.write(f"• **{nome_item}** (Quantidade: x{qtd})")
            if col_inv_botao.button("Usar", key=f"use_{nome_item}"):
                dados["inventario"][nome_item] -= 1
                if dados["inventario"][nome_item] <= 0:
                    del dados["inventario"][nome_item]
                st.balloons()
                st.success(f"🎉 Voucher Aplicado!")
                time.sleep(1)
                st.rerun()

# --- 4. ABA GERENCIAR HÁBITOS ---
with aba_gerenciar_habitos:
    st.write("### ➕ Cadastrar Novo Objetivo no Sistema")
    
    with st.form("formulario_habito", clear_on_submit=True):
        novo_nome = st.text_input("Nome do hábito/objetivo:")
        attr_selecionado = st.selectbox("Qual atributo esse hábito treina?", list(MAPA_ATRIBUTOS.keys()))
        
        dias_selecionados = st.multiselect(
            "Em quais dias da semana esse hábito deve aparecer na tela?",
            options=DIAS_SEMANA_PT,
            default=[dia_hoje_nome]
        )
        
        recorrencia_tipo = st.radio(
            "Regra de Repetição da Missão:",
            ("🔄 Recorrente (Aparece toda semana nestes dias)", "📌 Única (Executa uma vez e some após o dia acabar)")
        )
        is_recorrente = True if "Recorrente" in recorrencia_tipo else False
        
        col_xp, col_ouro = st.columns(2)
        recompensa_xp = col_xp.number_input("Recompensa de XP", min_value=10, max_value=1000, value=100, step=10)
        recompensa_ouro = col_ouro.number_input("Recompensa de Ouro", min_value=5, max_value=500, value=50, step=5)
        
        botao_salvar = st.form_submit_button("Sincronizar com o Sistema")
        
        if botao_salvar and novo_nome:
            if not dias_selecionados:
                st.error("🚨 Selecione ao menos um dia da semana para agendar a missão!")
            else:
                novo_id = int(time.time() * 1000) + random.randint(1, 99)
                
                # CORREÇÃO DEFINITIVA: Dicionário fechado perfeitamente com a chave '}' correta
                nova_missao = {
                    "id": novo_id,
                    "nome": novo_nome,
