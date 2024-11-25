import streamlit as st
from transformers import pipeline
from neo4j import GraphDatabase
from back import execute

# Load the Hugging Face question-answering model
st.write("Loading model...")
question_answering_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
st.write("Model loaded successfully!")

# Initialize Neo4j connection
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "12345neo"  # Replace with your Neo4j password

def execute_cypher_query(query):
    """Executes a Cypher query on the Neo4j database and returns the results."""
    try:
        with GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)) as driver:
            with driver.session() as session:
                return session.run(query).data()
    except Exception as e:
        return f"Error: {str(e)}"

def chat_with_neo4j(query):
    """
    Handles queries related to the Mahabharata by searching the Neo4j graph database.
    """
    result=execute(query)
    cypher_query = f"MATCH (n) WHERE n.name =~ '(?i).*{query}.*' RETURN n LIMIT 5"
    results = execute_cypher_query(cypher_query)
    if isinstance(result, str):  # Error handling   
        return result

    if results:
        response = "Here are the top results:\n" + "\n".join([result['n']['name'] for result in results])
    else:
        response = "No matching information found in the Mahabharata database."
    return response

# Streamlit UI
st.title("Mahabharata Question Answering Model")
st.write("Welcome! Ask any questions related to the Mahabharata.")

# User input
user_query = st.text_input("Enter your question:")

if st.button("Submit"):
    if user_query:
        st.write("Fetching response...")
        
        # Try to answer using Neo4j first
        graph_response = chat_with_neo4j(user_query)
        st.subheader("Graph Database Response:")
        st.write(graph_response)

        # Fallback to the Hugging Face model if no results found
        if "No matching information found" in graph_response or "Error" in graph_response:
            context = (
                "The Mahabharata is one of the two major Sanskrit epics of ancient India. "
                "It narrates the Kurukshetra War and the fates of the Kaurava and the Pandava princes. "
                "It also contains stories of Lord Krishna and other mythological tales."
            )
            model_response = question_answering_pipeline(
                question=user_query,
                context=context
            )
            st.subheader("Model Response:")
            st.write(model_response['answer'])
    else:
        st.warning("Please enter a question to proceed.")

# Option to clear chat
if st.button("Clear Chat"):
    st.caching.clear_cache()
    st.write("Chat cleared.")

st.write("---")
st.write("Developed by Rhythem Jain")
