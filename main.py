import streamlit as st
import json
import os
import random
from datetime import datetime

ARQUIVO_SAVE = "solo_leveling_save.json"

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

# Itens da loja focados em recompensas saudáveis de lazer na vida real
LOJA_SISTEMA = {
    "1": {"nome": "🧪 Poção de Mana (Ver 1 episódio de anime/série)", "custo": 50},
    "2": {"nome": "📜 Pergaminho de Retorno (Fim de semana livre de videogame)", "custo": 200},
    "3": {"nome": "🍖 Elixir da Juventude (Uma refeição livre/Lanche)", "custo": 300},
    "4": {"nome": "🔑 Chave de Dungeon (Comprar um mimo ou livro novo)", "custo": 500}
}

progresso_padrao = {
    "nome": "Sung Jin-Woo", "nivel": 1, "xp": 0, "ouro": 0,
    "atributos": {"Força": 10, "Inteligência": 10, "Vitalidade": 10, "Carisma": 10, "Agilidade": 10},
    "missoes": [
        {"id": 0, "nome": "💪 100 Flexões / Treino Físico", "xp": 100, "ouro": 50, "attr": "Força", "concluida_em": ""},
        {"id": 1, "nome": "📚 Estudar Python / Foco", "xp": 150, "ouro": 75, "attr": "Inteligência", "concluida_em": ""},
        {"id": 2, "nome": "👥 Tempo de Qualidade com a Família", "xp": 80, "ouro": 40, "attr": "Carisma", "concluida_em": ""}
    ],
    "inventario": {}
}

def carregar_dados():
    if os.path.exists(ARQUIVO_SAVE):
        try:
            with open(ARQUIVO_SAVE, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                if "nome" not in dados: dados["nome"] = "Sung Jin-Woo"
                if "missoes" not in dados: dados["missoes"] = progresso_padrao["missoes"].copy()
                if "inventario" not in dados: dados["inventario"] = {}
                return dados
        except:
            return progresso_padrao.copy()
    return progresso_padrao.copy()

def salvar_dados(dados):
    with open(ARQUIVO_SAVE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def calcular_xp_nec(nivel):
    return 100 + (nivel - 1) * 80

# Configuração da página mobile
st.set_page_config(page_title="Solo Leveling System", page_icon="⚡", layout="centered")

st.title("⚡ SOLO LEVELING SYSTEM")
dados = carregar_dados()
data_hoje = datetime.now().strftime("%Y-%m-%d")

# Abas do Aplicativo
aba_status, aba_missoes, aba_loja, aba_gerenciar_habitos = st.tabs([
    "👤 Status", 
    "🎯 Missões", 
    "🛒 Loja do Sistema", 
    "🛠️ Configurações"
])

with aba_status:
    st.subheader(f"Caçador: {dados['nome']}")
    
    # Formulário para alterar o nome do Caçador
    with st.expander("⚙️ Alterar Identidade do Caçador"):
        novo_nome_input = st.text_input("Insira seu nome real ou apelido:", value=dados["nome"])
        if st.button("Confirmar Despertar"):
            if novo_nome_input.strip():
                dados["nome"] = novo_nome_input.strip()
                salvar_dados(dados)
                st.success(f"Nome alterado para {dados['nome']}!")
                st.rerun()

    xp_nec = calcular_xp_nec(dados["nivel"])
    progresso_barra = min(dados["xp"] / xp_nec, 1.0)
    st.progress(progresso_barra, text=f"Nível {dados['nivel']} ({dados['xp']}/{xp_nec} XP)")
    
    col1, col2 = st.columns(2)
    col1.metric("💰 Ouro Disponível", f"{dados['ouro']} Ouro")
    col2.metric("📅 Data do Sistema", datetime.now().strftime('%d/%m/%Y'))
    
    st.write("### 📊 Status de Atributos")
    for attr, valor in dados["atributos"].items():
        st.write(f"**{attr}:** {valor}")

with aba_missoes:
    st.write("### Objetivos de Hoje")
    
    if not dados["missoes"]:
        st.info("Você não tem nenhuma missão cadastrada. Vá até a aba 'Configurações' para criar suas primeiras metas!")
    else:
        for m in dados["missoes"]:
            foi_concluida = m["concluida_em"] == data_hoje
            check = st.checkbox(m["nome"], value=foi_concluida, key=f"m_{m['id']}")
            
            if check and not foi_concluida:
                m["concluida_em"] = data_hoje
                dados["xp"] += m["xp"]
                dados["ouro"] += m["ouro"]
                dados["atributos"][m["attr"]] += 1
                
                while dados["xp"] >= calcular_xp_nec(dados["nivel"]):
                    dados["xp"] -= calcular_xp_nec(dados["nivel"])
                    dados["nivel"] += 1
                    st.balloons()
                    st.success(f"🎉 LEVEL UP! Nível {dados['nivel']}!\n{random.choice(FRASES_LEVEL_UP)}")
                    
                salvar_dados(dados)
                st.rerun()
                
            elif not check and foi_concluida:
                m["concluida_em"] = ""
                dados["xp"] = max(0, dados["xp"] - m["xp"])
                dados["ouro"] = max(0, dados["ouro"] - m["ouro"])
                dados["atributos"][m["attr"]] = max(10, dados["atributos"][m["attr"]] - 1)
                salvar_dados(dados)
                st.rerun()

with aba_loja:
    st.write(f"### 👛 Sua Carteira: **{dados['ouro']} Ouro**")
    st.write("---")
    
    st.write("### 🛍️ Itens Disponíveis para Compra")
    for k, item in LOJA_SISTEMA.items():
        col_item_info, col_item_botao = st.columns([3, 1])
        col_item_info.write(f"**{item['nome']}**  \n_Custo: 💰 {item['custo']} Ouro_")
        
        # Botão de compra
        if col_item_botao.button("Comprar", key=f"buy_{k}"):
            if dados["ouro"] >= item["custo"]:
                dados["ouro"] -= item["custo"]
                # Adiciona ao inventário
                dados["inventario"][item["nome"]] = dados["inventario"].get(item["nome"], 0) + 1
                salvar_dados(dados)
                st.toast(f"🛒 Adquirido: {item['nome']}!")
                st.rerun()
            else:
                st.error("🚨 Ouro insuficiente! Cumpra mais missões reais.")

    st.write("---")
    st.write("### 🎒 Seu Inventário (Vouchers Guardados)")
    
    if not dados["inventario"]:
        st.caption("Seu inventário está vazio. Trabalhe duro para comprar seus momentos de lazer!")
    else:
        for nome_item, qtd in list(dados["inventario"].items()):
            col_inv_info, col_inv_botao = st.columns([3, 1])
            col_inv_info.write(f"• **{nome_item}** (Quantidade: x{qtd})")
            
            # Botão para gastar/usar o voucher
            if col_inv_botao.button("Usar", key=f"use_{nome_item}"):
                dados["inventario"][nome_item] -= 1
                if dados["inventario"][nome_item] <= 0:
                    del dados["inventario"][nome_item]
                salvar_dados(dados)
                st.balloons()
                st.success(f"🎉 Aproveite o seu momento de lazer sem culpa! Recompensa resgatada.")
                time.sleep(1)
                st.rerun()

with aba_gerenciar_habitos:
    st.write("### ➕ Cadastrar Novo Objetivo no Sistema")
    
    with st.form("formulario_habito", clear_on_submit=True):
        novo_nome = st.text_input("Nome do hábito/objetivo (Ex: Ler 15 páginas, Beber 2L de água)")
        attr_selecionado = st.selectbox("Qual atributo esse hábito vai treinar?", list(MAPA_ATRIBUTOS.keys()))
        
        col_xp, col_ouro = st.columns(2)
        recompensa_xp = col_xp.number_input("Recompensa de XP", min_value=10, max_value=500, value=100, step=10)
        recompensa_ouro = col_ouro.number_input("Recompensa de Ouro", min_value=5, max_value=300, value=50, step=5)
        
        botao_salvar = st.form_submit_button("Sincronizar com o Sistema")
        
        if botao_salvar and novo_nome:
            novo_id = max([m["id"] for m in dados["missoes"]]) + 1 if dados["missoes"] else 0
            
            nova_missao = {
                "id": novo_id,
                "nome": novo_nome,
                "xp": int(recompensa_xp),
                "ouro": int(recompensa_ouro),
                "attr": MAPA_ATRIBUTOS[attr_selecionado],
                "concluida_em": ""
            }
            
            dados["missoes"].append(nova_missao)
            salvar_dados(dados)
            st.success(f"📜 Novo objetivo '{novo_nome}' adicionado com sucesso!")
            st.rerun()

    st.write("---")
    st.write("### ❌ Remover Objetivos Existentes")
    
    if not dados["missoes"]:
        st.caption("Nenhuma missão para exibir.")
    else:
        for idx, m in enumerate(dados["missoes"]):
            col_info, col_botao = st.columns([3, 1])
            col_info.write(f"**{m['nome']}**  \n_Atributo: {m['attr']} | XP: {m['xp']} | Ouro: {m['ouro']}_")
            
            if col_botao.button("Deletar", key=f"del_{m['id']}_{idx}"):
                dados["missoes"].remove(m)
                salvar_dados(dados)
                st.toast(f"❌ Missão removida!")
                st.rerun()
