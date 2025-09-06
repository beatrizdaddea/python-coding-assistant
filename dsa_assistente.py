import streamlit as st
from groq import Groq

# ----------------------------
# Configuração Inicial
# ----------------------------
st.set_page_config(
    page_title="DSA AI Coder",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_PROMPT = """
Você é o "DSA Coder", um assistente de IA especialista em programação...

INSTRUÇÕES IMPORTANTES:
1. Sempre inclua ao final da sua resposta uma seção de documentação com links relevantes
2. Use este formato exato para a documentação:

---
**📚 Documentação Sugerida:**
- [Python Official Documentation](https://docs.python.org/3/)
- [Tópico específico relacionado] (adicione links contextuais quando relevante)

*Consulte a documentação oficial para informações mais detalhadas.*
"""

# ----------------------------
# Funções Auxiliares
# ----------------------------
def init_sidebar() -> str:
    """Inicializa a barra lateral e retorna a API key informada pelo usuário."""
    with st.sidebar:
        st.title("🤖 DSA AI Coder")
        st.markdown("Um assistente de IA focado em programação Python.")

        api_key = st.text_input(
            "Insira sua API Key Groq", 
            type="password",
            help="Obtenha sua chave em https://console.groq.com/keys"
        )

        st.markdown("---")
        st.info("Desenvolvido para auxiliar dúvidas em Python. Sempre valide as respostas.")
        st.markdown("🔗 [Data Science Academy](https://www.datascienceacademy.com.br)")
        st.link_button("✉️ Suporte DSA", "mailto:suporte@datascienceacademy.com.br")

    return api_key


def init_client(api_key: str):
    """Inicializa o cliente da Groq API."""
    if not api_key:
        return None
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        st.sidebar.error(f"Erro ao inicializar cliente Groq: {e}")
        return None


def display_chat(messages: list):
    """Renderiza as mensagens do chat armazenadas na sessão."""
    for msg in messages:
        role_style = "color: green;" if msg["role"] == "assistant" else "color: blue;"
        with st.chat_message(msg["role"]):
            st.markdown(f"<span style='{role_style}'>{msg['content']}</span>", unsafe_allow_html=True)


def process_prompt(client, messages: list) -> str:
    """Processa as mensagens e retorna a resposta do modelo."""
    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}] + messages
    try:
        response = client.chat.completions.create(
            messages=messages_for_api,
            model="openai/gpt-oss-20b",
            temperature=0.7,
            max_tokens=2048,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Erro ao comunicar com API da Groq: {e}")
        return "⚠️ Não foi possível obter resposta no momento."


# ----------------------------
# Aplicação Principal
# ----------------------------
st.title("Data Science Academy - DSA AI Coder")
st.caption("Seu assistente pessoal para aprender Python 🐍")

if "messages" not in st.session_state:
    st.session_state.messages = []

groq_api_key = init_sidebar()
client = init_client(groq_api_key)

display_chat(st.session_state.messages)

if prompt := st.chat_input("Qual sua dúvida sobre Python?"):
    if not client:
        st.warning("⚠️ Insira sua API Key para começar.")
    else:
        # Armazena a mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                answer = process_prompt(client, st.session_state.messages)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

# Exportar conversa
st.download_button("📥 Exportar Conversa", str(st.session_state.messages), file_name="chat_dsa_ai_coder.json")

# Rodapé
st.markdown(
    """
    <div style="text-align: center; color: gray; font-size: 12px; margin-top: 20px;">
        <hr>
        <p>DSA AI Coder - Curso Gratuito de Fundamentos de Python | Data Science Academy</p>
    </div>
    """,
    unsafe_allow_html=True
)
