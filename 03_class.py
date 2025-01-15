import streamlit as st

VALID_FILE_TIPS = [
    'site', 'Youtube', 'PDF', 'CSV', 'TXT'
]

VALID_MODELS = {
    'Groq': {'modelos': ['gemma2-9b-it', 'llama-3.3-70b-versatile']},
    'OpenAI': {'modelos': ['gpt-4o-mini', 'gpt-4o']},
    'Gemini': {'modelos': ['gemini-1.5-flash', 'gemini-1.5-flash-8b']}
}


def chat_page():
    st.header('Bem vindo ao oraculo', divider=True)
    messages = st.session_state.get('messages', [])

    for message in messages:
        chat = st.chat_message(message[0])
        chat.markdown(message[1])

    input_user = st.chat_input('fale com o oráculo')

    if input_user:
        messages.append(('user', input_user))

        st.session_state['messages'] = messages
        st.rerun()


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


def main():
    chat_page()
    with st.sidebar:
        sidebar()


if __name__ == '__main__':
    main()
