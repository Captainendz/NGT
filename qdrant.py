import os
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import Qdrant
from dotenv import load_dotenv

# Define your OpenAI API key
api_key = "your API key here"

def load_file(file_path: str):
    """Load the file using Langchain's TextLoader."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File does not exist: {file_path}")

    # Initialize TextLoader for the specific text file
    loader = TextLoader(file_path=file_path, encoding='utf-8')
    loaded_docs = loader.load()
    print(f"Loaded {len(loaded_docs)} documents from {file_path}")

    # Print the content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        print(f"\nContent of {file_path}:\n{content}")

    return loaded_docs

def embed_documents(docs, api_key):
    """Embed the loaded documents using OpenAI and index into Qdrant."""
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    print(f"Total document chunks created: {len(splits)}")

    if not splits:
        print("No documents were split. Please check the input documents.")
        return

    # Ensure IDs are generated
    for i, doc in enumerate(splits):
        if not doc.metadata.get("id"):
            doc.metadata["id"] = f"doc_{i}"

    # Create OpenAI embeddings
    embedding_model = OpenAIEmbeddings(openai_api_key=api_key)
   #vectors = [embedding_model.embed_text(doc.page_content) for doc in splits]

    url = "http://localhost:6333/"
    Qdrant.from_documents(
        splits,
        embedding_model,
        url=url,
        collection_name="my_documents",
    )
    print("Documents embedded and indexed in Qdrant.")

def indexFile(filePath):
    """Load and embed the file, returning an 'Indexed' message upon completion."""
    try:
        # Load the file
        loaded_docs = load_file(filePath)
        
        # Embed the loaded documents
        embed_documents(loaded_docs, api_key)
        
        return "Indexed"
    except Exception as e:
        return str(e)

# Get the absolute path to the text file
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "3GPP_raw_text.txt")

print(indexFile(file_path))
