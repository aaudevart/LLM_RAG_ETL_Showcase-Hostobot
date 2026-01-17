import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_neo4j import Neo4jVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import init_chat_model

HOSPITAL_QA_EMBEDDING_MODEL = os.getenv("HOSPITAL_QA_EMBEDDING_MODEL")
HOSPITAL_QA_MODEL = os.getenv("HOSPITAL_QA_MODEL")    
HOSPITAL_QA_PROVIDER = os.getenv("HOSPITAL_QA_PROVIDER")

if HOSPITAL_QA_PROVIDER == "google_genai":
    embedding = GoogleGenerativeAIEmbeddings(model=os.getenv("HOSPITAL_QA_EMBEDDING_MODEL"),
                                            task_type="RETRIEVAL_DOCUMENT")
else:
    embedding = OpenAIEmbeddings()

neo4j_vector_index = Neo4jVector.from_existing_graph(
    embedding=embedding,
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
    index_name="reviews",
    node_label="Review",
    text_node_properties=[
        "physician_name",
        "patient_name",
        "text",
        "hospital_name",
    ],
    embedding_node_property="embedding",
)

retriever=neo4j_vector_index.as_retriever(k=12)

review_template = """Your task is to analyze patient reviews to answer questions about their experiences at a hospital. Use the provided context to guide your responses. Be as thorough as possible, but only rely on the information given—do not infer or invent details. If the answer isn't in the context, say you don't know."""

review_prompt = ChatPromptTemplate.from_messages([
    ("system", review_template+ "\n\n{context}"),
    ("human", "{question}")
])

chat_qa_model = init_chat_model(model_provider=HOSPITAL_QA_PROVIDER,
                                    model=HOSPITAL_QA_MODEL,
                                    temperature=0)


reviews_vector_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | review_prompt
    | chat_qa_model
)