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

# --- INICIALIZAÇÃO E ARMAZENAMENTO SEGURO NA NUVEM ---
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

# --- CONFIGURAÇÃO DA INTERFACE MOBILE ---
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

# --- SEÇÃO 2: MISSÕES DE HOJE (Filtro por Data Real) ---
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
                
                # Ação Concluir
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
                        st.success(f"🎉 LEVEL UP NÍVEL {dados['nivel']}!\n{random.choice(FRASES_LEVEL_UP)}")
                    time.sleep(1)
                    st.rerun()
                
                # Ação Penalidade
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

# --- SEÇÃO 5: EXCLUSÃO E RESET CRÍTICO ---
elif opcao_menu == "❌ Configurações Críticas":
    st.header("❌ REMOVER MISSÕES")
    
    if not dados["missoes"]:
        st.caption("Nenhum hábito cadastrado para deletar.")
    else:
        for idx, m in enumerate(dados["missoes"]):
            agenda_str = ", ".join([d[:3] for d in m.get("dias", [])])
            st.write(f"**{m['nome']}** ({m['attr']} | {agenda_str})")
            
            # CORREÇÃO DEFINITIVA PARA CELULAR: Botão limpo sem conflito de loops de aba
            if st.button("Excluir Permanentemente", key=f"del_m_{m['id']}_{idx}"):
                dados["missoes"].remove(m)
                st.toast("❌ Hábito removido!")
                time.sleep(0.5)
                st.rerun()
            st.write("---")
            
    st.header("🚨 REINICIAR NÍVEL E STATUS")
    st.warning("Isso redefinirá seu Nível para 1, zerará moedas/XP e voltará os Atributos para 10. Seus hábitos salvos serão mantidos.")
    confirmacao_reset = st.checkbox("Confirmo que quero zerar o nível do meu caçador.", key="chk_reset_mobile")
    
    # CORREÇÃO DEFINITIVA PARA CELULAR: Botão limpo sem conflito de loops de aba
