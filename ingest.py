#Import Libraries
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils import embedding_functions
import os

#Ingestion Function
def ingest_pdf(pdf_path):

    # Step1 Load the pdf
    # Points to your PDF.
    loader = PyPDFLoader(pdf_path)

    # Converts PDF pages into Langchain Documents.
    documents = loader.load()
    print("Pages Loaded: ", len(documents))


    #Step2 Chunking (Breaking the Large File into the small piece(chunk))
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )

    chunks = splitter.split_documents(documents)
    print("Chunks Created: ", len(chunks)) #number of Chunks


    #Step3 Embedding (Convert the chunks into Vector(Numerical Representation))

    client = chromadb.PersistentClient(path="./vectordb")

    embedding_function = embedding_functions.DefaultEmbeddingFunction()

    try:
        client.delete_collection("java_notes")
    except:
        pass

    collection_name = os.path.splitext(
    os.path.basename(pdf_path)
    )[0].lower()

    collection_name = collection_name.replace("-", "_").replace(" ", "_")

    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )

    # Step4: Store Chunks

    documents_to_store = []
    ids = []

    for i, chunk in enumerate(chunks):
        clean_text = " ".join(chunk.page_content.split())
        documents_to_store.append(clean_text)
        ids.append(f"chunk_{i}")

    collection.add(
        documents=documents_to_store,
        ids=ids
    )

    print("All Chunks Stored Successfully")

    # Step5: Verify Storage

    print("Total Documents in Collection:",
        collection.count())
    
    return "PDF Processing Completed Successfully!"