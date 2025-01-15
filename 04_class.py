import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

VALID_FILE_TIPS = [
    'site', 'Youtube', 'PDF', 'CSV', 'TXT'
]

VALID_MODELS = {
    'Groq':
        {
            'modelos': ['gemma2-9b-it', 'llama-3.3-70b-versatile'],
            'chat': ChatGroq
        },
    'Gemini':
        {
            'modelos': ['gemini-1.5-flash', 'gemini-1.5-flash-8b'],
            'chat': ChatGoogleGenerativeAI
        }
}

MEMORY = ConversationBufferMemory()


def load_model(provider, model, api_key):
    if api_key:
        chat = VALID_MODELS[provider]['chat'](model=model, api_key=api_key)
        st.session_state['chat'] = chat
    else:
        st.warning('É necessário inserir uma API Key para inicializar o oráculo')


def chat_page():
    st.header('Bem vindo ao oraculo', divider=True)

    chat_model = st.session_state.get('chat')
    memory = st.session_state.get('memory', MEMORY)

    for message in memory.buffer_as_messages:
        chat = st.chat_message(message.type)
        chat.markdown(message.content)

    input_user = st.chat_input('fale com o oráculo')

    if input_user:
        chat = st.chat_message('human')
        chat.markdown(input_user)

        chat = st.chat_message('ai')
        response = chat.write_stream(chat_model.stream(input_user))

        memory.chat_memory.add_user_message(input_user)
        memory.chat_memory.add_ai_message(response)

        st.session_state['memory'] = memory


def sidebar():
    tabs = st.tabs(['upload de arquivos', 'seleção de modelos'])
    with tabs[0]:
        file_types = st.selectbox(
            'selecione o tipo de arquivo', VALID_FILE_TIPS
            )

        if file_types == 'site':
            site_url = st.chat_input('informe sua URL')

        if file_types == 'Youtube':
            video_url = st.chat_input('informe sua URL')

        if file_types == 'PDF':
            pdf_archive = st.file_uploader(
                'faça o upload do arquivo pdf', type=['.pdf']
            )

        if file_types == 'CSV':
            pdf_archive = st.file_uploader(
                'faça o upload do arquivo pdf', type=['.csv']
            )

        if file_types == 'TXT':
            pdf_archive = st.file_uploader(
                'faça o upload do arquivo pdf', type=['.txt']
            )

    with tabs[1]:
        provider = st.selectbox(
            'selecione a IA',
            VALID_MODELS.keys()
        )

        model_type = st.selectbox(
            'selecione o modelo de IA', VALID_MODELS[provider]['modelos']
        )

        api_key = st.text_input(
            f'adicione a api Key para o provedor {provider}',
            value=st.session_state.get(f'api_key_{provider}')
        )

        st.session_state[f'api_key_{provider}'] = api_key

        if st.button('inicializar Oráculo', use_container_width=True):
            load_model(provider, model_type, api_key)


def main():
    chat_page()
    with st.sidebar:
        sidebar()


if __name__ == '__main__':
    main()
