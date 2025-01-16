import streamlit as st
import tempfile
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from loaders import *
from langchain.prompts import ChatPromptTemplate

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


def load_file(file_type, file):
    if file_type == 'site':
        document = load_site(file)
    elif file_type == 'Youtube':
        document = load_video(file)
    elif file_type == 'PDF':
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp:
            temp.write(file.read())
            temp_name = temp.name
        document = load_pdf(temp_name)
    elif file_type == 'CSV':
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
            temp.write(file.read())
            temp_name = temp.name
        document = load_csv(temp_name)
    elif file_type == 'PDF':
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp:
            temp.write(file.read())
            temp_name = temp.name
        document = load_pdf(temp_name)
    return document


def load_model(provider, model, api_key, file_type, file):

    document = load_file(file_type, file)

    system_message = '''Você é um assistente amigável chamado Oráculo.
    Você possui acesso às seguintes informações vindas 
    de um documento {}: 

    ####
    {}
    ####

    Utilize as informações fornecidas para basear as suas respostas.

    Sempre que houver $ na sua saída, substita por S.

    Se a informação do documento for algo como "Just a moment...Enable JavaScript and cookies to continue"
    sugira ao usuário carregar novamente o Oráculo!'''.format(file_type, document)

    template = ChatPromptTemplate.from_messages([
        ('system', system_message),
        ('placeholder', '{chat_history}'),
        ('user', '{input}')
    ])

    chat = VALID_MODELS[provider]['chat'](model=model, api_key=api_key)
    chain = template | chat
    st.session_state['chain'] = chain


def chat_page():
    st.header('Bem vindo ao oraculo', divider=True)

    chain = st.session_state.get('chain')
    if chain is None:
        st.error('carregue o oráculo!')
        st.stop()
    memory = st.session_state.get('memory', MEMORY)

    for message in memory.buffer_as_messages:
        chat = st.chat_message(message.type)
        chat.markdown(message.content)

    input_user = st.chat_input('fale com o oráculo')

    if input_user:
        chat = st.chat_message('human')
        chat.markdown(input_user)

        chat = st.chat_message('ai')
        response = chat.write_stream(chain.stream({
            'input': input_user, 'chat_history': memory.buffer_as_messages
            }))

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
            file = st.text_input('informe sua URL')

        if file_types == 'Youtube':
            file = st.text_input('informe sua URL')

        if file_types == 'PDF':
            file = st.file_uploader(
                'faça o upload do arquivo pdf', type=['.pdf']
            )

        if file_types == 'CSV':
            file = st.file_uploader(
                'faça o upload do arquivo pdf', type=['.csv']
            )

        if file_types == 'TXT':
            file = st.file_uploader(
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
            load_model(provider, model_type, api_key, file_types, file)
        if st.button('remover histórico', use_container_width=True):
            st.session_state['memory'] = MEMORY


def main():
    with st.sidebar:
        sidebar()
    chat_page()


if __name__ == '__main__':
    main()
