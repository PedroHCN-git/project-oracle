from langchain_community.document_loaders import WebBaseLoader, YoutubeLoader, CSVLoader, PyPDFLoader, TextLoader
from dotenv import load_dotenv
import os

load_dotenv()

site_url = 'https://asimov.academy/'


def load_site():
    loader = WebBaseLoader(site_url)
    documents_list = loader.load()
    document = '\n\n'.join([doc.page_content for doc in documents_list])
    return document


video_url = 'q_sUW_e9w74&t'


def load_video(video_url):
    loader = YoutubeLoader(video_url, add_video_info=False, language=['pt'])
    documents_list = loader.load()
    document = '\n\n'.join([doc.page_content for doc in documents_list])
    return document


path = '.\\archives\\example.csv'


def load_csv(path):
    loader = CSVLoader(file_path=path)
    documents_list = loader.load()
    document = '\n\n'.join([doc.page_content for doc in documents_list])
    return document


print(load_csv(path))
