from langchain_qdrant import Qdrant
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
#from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.prompts import PromptTemplate
from qdrant_client import QdrantClient
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub
from langchain.chains import LLMChain

# OpenAI API key for ChatOpenAI model
openai_api_key = "your API key here"

# Initialize ChatOpenAI model
chat_model = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo")

# Initialize Qdrant client
client = QdrantClient("http://localhost:6333")

# Initialize OpenAI embeddings (optional, if needed)
embeddings = OpenAIEmbeddings(api_key=openai_api_key)

# Initialize Qdrant vector store
vector_store = Qdrant(
    embeddings=embeddings,
    client=client,
    collection_name="my_documents"
)

# Define a prompt template
template = """You are a helpful assistant. The user has asked a question:
{input}
Please provide a detailed and accurate response."""

prompt = PromptTemplate(template=template, input_variables=["input"])

# Create a retriever from the vector store
retriever = vector_store.as_retriever()

# Create the combine_docs_chain using create_stuff_documents_chain
retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
combine_docs_chain = create_stuff_documents_chain(chat_model, retrieval_qa_chat_prompt)

# Create the retrieval chain
retrieval_chain = LLMChain(llm=chat_model, prompt=prompt)
# Function to handle user queries
def handle_query(query):
    response = retrieval_chain.run(query)
    return response

# Example usage
if __name__ == "__main__":
    query = "What are QoS rules?"
    response = handle_query(query)
    print("User Query:", query)
    print("Response:", response)
 