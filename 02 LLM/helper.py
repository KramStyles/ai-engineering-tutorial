from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

from config import OPEN_AI_KEY as api_key

url = "https://365datascience.com/upcoming-courses/"
loader = WebBaseLoader(url)
raw_documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(raw_documents)

# gpt-4o-mini
embeddings = OpenAIEmbeddings(openai_api_key=api_key)
vectorstore = FAISS.from_documents(documents, embeddings)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

qa = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=api_key, temperature=0),
    retriever=vectorstore.as_retriever(),
    memory=memory
)

# query = "What is the next course to be uploaded on the 365 Data Science website?"
# answer was 'I don't know.'
query = "What course has the highest rating on the 365 Data Science website?"
result = qa({"question": query})
print(result["answer"])