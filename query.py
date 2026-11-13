import chromadb
from chromadb.utils import embedding_functions

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Load Environment Variables
load_dotenv()

# Initialize LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.2,
    max_tokens=1024
)

# Initialize ChromaDB

client = chromadb.PersistentClient("./vectordb")

# embedding_function = embedding_functions.DefaultEmbeddingFunction()


# Query Function

def ask_question(question, collection_name):
    collection = client.get_collection(
    name=collection_name
    )

    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    # Extract Relevant Documents
    documents = results["documents"][0]

    context = "\n\n".join(documents)

    # Create Prompt

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are an intelligent AI assistant.

            Answer the user's question using the
            provided PDF context.

            Instructions:
            1. Give clear and accurate answers.
            2. Explain concepts in simple language.
            3. If the answer is not available in the
            context, say that it is not available
            in the uploaded PDF.
            4. Do not make up information.

            Context:
            {context}
            """
        ),
        (
            "human",
            "{question}"
        )
    ])

    # Create LLM Chain

    chain = prompt | llm

    # Generate AI Answer

    response = chain.invoke({
        "context": context,
        "question": question
    })

    # Return Answer
    return response.content
    
