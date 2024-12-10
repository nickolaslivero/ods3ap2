import streamlit as st
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="lm-studio")

if "history" not in st.session_state:
    st.session_state["history"] = [
        {"role": "system", "content": """Você é um assistente rápido, eficiente e especializado em toadas de boi-bumbá e cultura amazônica brasileira.
         Você conhece profundamente os bois garantido, e o boi Caprichoso, e o festival de Parintins.
         Você também sabe criar musicas referentes às toadas.
         SEMPRE que o usuário pedir uma musica, faça uma breve musica com 3 a 4 versos no máximo.
         Lembre-se que SEMPRE o boi Garantido é Vermelho e Branco, e o boi Caprichoso é o Azul e Preto e nunca esqueça disso jamais."""},
        {"role": "assistant", "content": "Olá! Sou um assistente que conhece profundamente as toadas de boi-bumbá e a cultura amazônica. Como posso ajudar hoje?"}
    ]

st.title("Chatbot de Toadas Amazônicas 🎵")
st.subheader("Converse sobre a cultura amazônica e toadas de boi-bumbá!")

def render_chat():
    for message in st.session_state["history"]:
        if message["role"] == "user":
            st.markdown(f"**Você:** {message['content']}")
        elif message["role"] == "assistant":
            st.markdown(f"**Assistente:** {message['content']}")


def send_message():
    user_input = st.session_state.input_text.strip()
    if user_input:
        st.session_state["history"].append({"role": "user", "content": user_input})


        with st.spinner("Gerando resposta..."):
            completion = client.chat.completions.create(
                model="bois/unsloth",
                messages=st.session_state["history"],
                temperature=0.7,
                stream=True,
            )

            new_message = {"role": "assistant", "content": ""}


            placeholder = st.empty()
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    new_message["content"] += chunk.choices[0].delta.content
                    placeholder.markdown(f"**Assistente:** {new_message['content']}")

            st.session_state["history"].append(new_message)

        st.session_state["input_text"] = ""
        placeholder.empty()

render_chat()

st.text_input(
    "Digite sua mensagem:",
    key="input_text",
    placeholder="Fale sobre uma toada clássica ou pergunte algo!",
    on_change=send_message
)
