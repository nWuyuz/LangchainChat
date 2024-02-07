#You need to assign a file to search for. Check searchforlocation.py
#The Chatbot will look for the similar context
import os

from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

run=True

api = "https://api.openai.com/"
# api = ""
key = ""

# def
text_location = []
text_files = []
documents=""

def find_text_files():
    for root, _, files in os.walk('C:Users/USER/desktop/pysearch'):
        for file in files:
            if file.endswith("txt"):
                file_path = os.path.join(root, file).replace("\\","/")
                text_location.append(file_path)


def load_text_files(file_paths):
    for i in range(10):
        loader = TextLoader(text_location, encoding='utf-8')
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=1)
        docs = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings(openai_api_base=api,
                                      openai_api_key=key)

        db = FAISS.from_documents(docs, embeddings)
        db.save_local("faiss_index")

        message = input('what are you looking for:')
        docs = db.similarity_search(message)

        print(docs[0].page_content)


def search(db):
    while True:
        message = input('what are you looking for(type "quit" to quit):')
        if message.lower() == 'quit':
            run=False

        try:
            results = db.similarity_search(message)
            if results:
                print(results[0].page_content)
            else:
                print("No matching documents found.")
        except Exception as e:
            print(f"Error during search: {e}")


# main
def main():
    text_files = find_text_files()
    if not text_files:
        print("No text files found.")
        run=False

    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=1)#lower chunk size might cause the bot to get some info missing, but large chunk may cause the answer to become too vague
    docs = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings(openai_api_base=api, openai_api_key=key)

    docs = FAISS.from_documents(docs, embeddings)
    docs.save_local("faiss_index")

    search(docs)

while run:
    main()
