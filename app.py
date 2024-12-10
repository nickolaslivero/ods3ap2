import streamlit as st
from openai import OpenAI

# Configuração do cliente LM Studio
client = OpenAI(base_url="http://localhost:8000/v1", api_key="lm-studio")

# Inicializa o histórico de mensagens
if "history" not in st.session_state:
    st.session_state["history"] = [
        {"role": "system", "content": """Você é um assistente especializado em toadas de boi-bumbá e cultura amazônica brasileira.
         Voce conhece profundamente os bois garantido, e o boi Caprichoso, e o festival de Parintins
         Você também sabe criar musicas referentes às toadas. SEMPRE que o usuário pedir uma musica, faça com pelo menos 4 versos referentes ao boi requerido."""},
        {"role": "assistant", "content": "Olá! Sou um assistente que conhece profundamente as toadas de boi-bumbá e a cultura amazônica. Como posso ajudar hoje?"}
    ]

# Configuração da página
st.title("Chatbot de Toadas Amazônicas 🎵")
st.subheader("Converse sobre a cultura amazônica e toadas de boi-bumbá!")

# Exibe o histórico de conversas
def render_chat():
    for message in st.session_state["history"]:
        if message["role"] == "user":
            st.markdown(f"**Você:** {message['content']}")
        elif message["role"] == "assistant":
            st.markdown(f"**Assistente:** {message['content']}")

# Caixa de entrada de mensagens
def send_message():
    user_input = st.session_state.input_text.strip()
    if user_input:
        # Armazena a mensagem do usuário
        st.session_state["history"].append({"role": "user", "content": user_input})


        # Solicita a resposta do assistente
        with st.spinner("Gerando resposta..."):
            completion = client.chat.completions.create(
                model="bois/unsloth",
                messages=st.session_state["history"],
                temperature=0.7,
                stream=True,
            )

            new_message = {"role": "assistant", "content": ""}

            # Exibe tokens em tempo real
            placeholder = st.empty()
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    new_message["content"] += chunk.choices[0].delta.content
                    placeholder.markdown(f"**Assistente:** {new_message['content']}")

            st.session_state["history"].append(new_message)

        # Limpa a entrada de texto de forma segura
        st.session_state["input_text"] = ""  # Evita modificar o widget diretamente
        placeholder.empty()  # Limpa o placeholder ao final da resposta

# Renderiza o histórico inicial
render_chat()

# Entrada de texto do usuário
st.text_input(
    "Digite sua mensagem:", 
    key="input_text", 
    placeholder="Fale sobre uma toada clássica ou pergunte algo!",
    on_change=send_message
)
