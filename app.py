from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
import os
import pinecone 
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


PINECONE_API_KEY = os.getenv('47dee970-f3c0-41bb-8ba5-a9984d40b98d')
PINECONE_ENV = os.getenv('us-west4-gcp-free')
# OPENAI_API_KEY = os.getenv('bjhDW59OrAxactxONM62T3BlbkFJgO0oFHE2yhYp7WLha2SG')
openai_api_key = "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"
# os.environ['OPENAI_API_KEY'] = "bjhDW59OrAxactxONM62T3BlbkFJgO0oFHE2yhYp7WLha2SG"


def doc_preprocessing():
    loader = DirectoryLoader(
        'data/',
        glob='**/*.md',     # only the PDFs
        show_progress=True
    )
    docs = loader.load()
    # st.info(docs)
    text_splitter = CharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=120
    )
    docs_split = text_splitter.split_documents(docs)
    return docs_split

@st.cache_resource
def embedding_db():
    # we use the openAI embedding model
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    pinecone.init(
        api_key='47dee970-f3c0-41bb-8ba5-a9984d40b98d',      
	    environment='us-west4-gcp-free'
    )
    index = pinecone.Index('myself')
    st.info("works")
    docs_split = doc_preprocessing()
    doc_db = Pinecone.from_documents(
        docs_split, 
        embeddings, 
        index_name='myself'
    )
    
    return doc_db

llm = ChatOpenAI(openai_api_key=openai_api_key)
doc_db = embedding_db()

def retrieval_answer(query):
    qa = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type='stuff',
    retriever=doc_db.as_retriever(),
    )
    query = query
    result = qa.run(query)
    return result

def main():
    st.title("Question and Answering App powered by LLM and Pinecone")
    text_input = st.text_input("Ask your query...") 
    if st.button("Ask Query"):
        if len(text_input)>0:
            st.info("Your Query: " + text_input)
            answer = retrieval_answer(text_input)
            st.success(answer)

if __name__ == "__main__":
    main()

    







