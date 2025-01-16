from langchain_community.document_loaders import WebBaseLoader, YoutubeLoader, CSVLoader, PyPDFLoader, TextLoader
from dotenv import load_dotenv

load_dotenv()


def load_site(site_url):
    loader = WebBaseLoader(site_url)
    documents_list = loader.load()
    document = '\n\n'.join([doc.page_content for doc in documents_list])
    return document


def load_video(video_url):
    loader = YoutubeLoader(video_url, add_video_info=False, language=['pt'])
    documents_list = loader.load()
    document = '\n\n'.join([doc.page_content for doc in documents_list])
    return document


def load_csv(path):
    loader = CSVLoader(file_path=path, encoding='UTF8')
    documents_list = loader.load()
    document = '\n\n'.join([doc.page_content for doc in documents_list])
    return document


def load_pdf(path):
    loader = PyPDFLoader(file_path=path)
    documents_list = loader.load()
    document = '\n\n'.join([doc.page_content for doc in documents_list])
    return document


def load_text(path):
    loader = TextLoader(file_path=path, encoding='UTF8')
    documents_list = loader.load()
    document = '\n\n'.join([doc.page_content for doc in documents_list])
    return document
