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

progresso_padrao = {
    "nome": "Sung Jin-Woo", "nivel": 1, "xp": 0, "ouro": 0,
    "atributos": {"Força": 10, "Inteligência": 10, "Vitalidade": 10, "Carisma": 10, "Agilidade": 10},
    "missoes": [
        {"id": 0, "nome": "💪 100 Flexões / Treino Físico", "xp": 100, "ouro": 50, "attr": "Força", "concluida_em": ""},
        {"id": 1, "nome": "📚 Estudar Python / Foco", "xp": 150, "ouro": 75, "attr": "Inteligência", "concluida_em": ""},
        {"id": 2, "nome": "👥 Tempo de Qualidade com a Família", "xp": 80, "ouro": 40, "attr": "Carisma", "concluida_em": ""}
    ]
}

def carregar_dados():
    if os.path.exists(ARQUIVO_SAVE):
        try:
            with open(ARQUIVO_SAVE, 'r', encoding='utf-8') as f:
                return json.load(f)
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

# Criando as abas do Aplicativo móvel
aba_status, aba_missoes = st.tabs(["👤 Status do Caçador", "🎯 Missões Diárias"])

with aba_status:
    st.subheader(f"Caçador: {dados['nome']}")
    xp_nec = calcular_xp_nec(dados["nivel"])
    
    # Barra de Progresso do Level
    progresso_barra = min(dados["xp"] / xp_nec, 1.0)
    st.progress(progresso_barra, text=f"Nível {dados['nivel']} ({dados['xp']}/{xp_nec} XP)")
    
    col1, col2 = st.columns(2)
    col1.metric("💰 Ouro do Sistema", f"{dados['ouro']} Ouro")
    col2.metric("📅 Data do Calendário", datetime.now().strftime('%d/%m/%Y'))
    
    st.write("### 📊 Atributos Mentais e Físicos")
    for attr, valor in dados["atributos"].items():
        st.write(f"**{attr}:** {valor}")

with aba_missoes:
    st.write("### Objetivos Agendados para Hoje")
    
    for m in dados["missoes"]:
        # Se a missão já foi feita hoje, ela começa marcada
        foi_concluida = m["concluida_em"] == data_hoje
        
        # Checkbox interativo na tela do celular
        check = st.checkbox(m["nome"], value=foi_concluida, key=f"m_{m['id']}")
        
        # Se o usuário clicar para marcar a missão
        if check and not foi_concluida:
            m["concluida_em"] = data_hoje
            dados["xp"] += m["xp"]
            dados["ouro"] += m["ouro"]
            dados["atributos"][m["attr"]] += 1
            
            # Verificação de Level Up
            while dados["xp"] >= calcular_xp_nec(dados["nivel"]):
                dados["xp"] -= calcular_xp_nec(dados["nivel"])
                dados["nivel"] += 1
                st.balloons() # Animação festiva na tela do celular
                st.success(f"🎉 LEVEL UP! Você atingiu o Nível {dados['nivel']}!\n{random.choice(FRASES_LEVEL_UP)}")
                
            salvar_dados(dados)
            st.rerun()
            
        # Se o usuário desmarcar a missão (reverter o ponto do dia)
        elif not check and foi_concluida:
            m["concluida_em"] = ""
            dados["xp"] = max(0, dados["xp"] - m["xp"])
            dados["ouro"] = max(0, dados["ouro"] - m["ouro"])
            dados["atributos"][m["attr"]] = max(10, dados["atributos"][m["attr"]] - 1)
            salvar_dados(dados)
            st.rerun()
