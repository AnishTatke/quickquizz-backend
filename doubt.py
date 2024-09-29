
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os

from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API")


# BEFORE COMMITTING
CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Context: Closely matching context to the query:
{context}

Task: Answer the given query: '{query}' from the provided context with a relevant response. Consider contextual similarity, key concepts, and overall intent.

Instructions:
1. Carefully review each chunk in the context.
2. You can combine a couple of chunks together if they semantically answer the query better. 
3. If no suitable match is found, return "not found".
4. Only use terms provided in the context. Do not generate or invent new terms.
5. Return only the standard goal term without any reasoning, explanation or special characters

Important:
- Prioritize an accurate and relevant response to the query, derived directly from the context.
- Avoid any forced matching. If the context does not contain relevant information, simply return "not found".
- Ensure the response is clear, concise, and directly addresses the query.t.

Question: '{query}'
Answer:
"""

def answer_doubt(query: str, k: int = 20):
    
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    model = ChatOpenAI(model_name="gpt-4")

    top_k_occurrences = db.similarity_search_with_relevance_scores(query, k)   
    context_entries = [f"{i+1}. {doc.page_content}" for i, (doc, _score) in enumerate(top_k_occurrences)]
    context_text = "\n---\n".join(context_entries)
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, query=query)
    response_text = model.invoke(prompt).content
    return response_text