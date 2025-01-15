import streamlit as st

EXAMPLE_MESSAGES = [
    ('user', 'olá'),
    ('assistent', 'tudo bem?'),
    ('user', 'tudo ótimo')
]


def chat_page():
    st.header('Bem vindo ao oraculo', divider=True)
    messages = st.session_state.get('messages', EXAMPLE_MESSAGES)

    for message in messages:
        chat = st.chat_message(message[0])
        chat.markdown(message[1])

    input_user = st.chat_input('fale com o oráculo')

    if input_user:
        messages.append(('user', input_user))

        st.session_state['messages'] = messages
        st.rerun()


def main():
    chat_page()


if __name__ == '__main__':
    main()
