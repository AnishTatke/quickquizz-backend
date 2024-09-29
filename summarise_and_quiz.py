import os
import re
import json

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API")

# Function to summarize a text chunk
def summarize_text(model, text_chunk, summary_type):
    
    PROMPT_TEMPLATE = """
    Task: Summarize the '{text_chunk}' in the '{summary_type}' style and return the summary as a JSON object.

    Requirements:
    1. Generate a 'title' and 'content' based on the summarized text.
    - The 'title' should reflect the main idea of the summary and be written in capital letters.
    - The 'content' should contain the summarized text of the given {text_chunk}.
    2. Follow these formatting rules:
    - If the {text_chunk} has a conclusive tone, use 'CONCLUSION' as the 'title'.
    - Start the 'content' with a blank line after the 'title'.
    - If applicable, use bullet points in the 'content' unless it is the introductory slide.
    - Do not use bullet points for the introductory slide; keep it in paragraph form.
    - Do not put any special characters and '\n' in the response.

    Output a JSON object where each we have 2 properties: 'title' and 'content'. is a question object as specified above. Ensure that the content is aligned with the difficulty level specified by the {summary_type}.
    """
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(text_chunk=text_chunk, summary_type=summary_type)
    response_text = model.invoke(prompt).content
    return response_text

# Function to create a quiz based on a given context
def create_quiz(model, context,mode):
    
    PROMPT_TEMPLATE = """
    Task: Create a quiz of 10 multiple choice questions in json format for the given context:
    {context} and keep the difficulty level as {mode}.

    Each question should contain the following fields:
    1. `"question"`: A string containing the question prompt.
    2. `"options"`: A list of four strings, each representing a possible answer choice.
    3. `"answer"`: An integer (0, 1, 2, or 3) representing the index of the correct option in the `options` list.
    4. `"justification"`: A string providing a brief explanation of why the correct answer is correct.

    Output the quiz as a JSON object with a `"questions"` array, where each array item is a question object as specified above. Ensure that all questions are factually accurate, drawn from the `context`, and align with the difficulty level specified by the {mode}.
    """
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context, mode=mode)
    quiz = model.invoke(prompt).content
    return quiz

# Function to handle multiple chunks of text and summarize them
def summarize_document(model, document_text, chunk_size=4000, summary_type="detailed"):
    # Split the document into smaller chunks based on the token limit
    chunks = [document_text[i:i + chunk_size] for i in range(0, len(document_text), chunk_size)]
    
    summaries = []
    for i, chunk in enumerate(chunks):
        print(f"Summarizing chunk {i+1}/{len(chunks)}...")
        summary = summarize_text(model, chunk, summary_type=summary_type)
        summaries.append(summary)

    combined_summary = " ".join(summaries)
    # final_summary = summarize_text(model, combined_summary, summary_type="concise and introductory slide which covers the overall intent with 'title':'INTRODUCTION' and restrict the 'content' to 80 words.")
    # summaries.insert(0, final_summary)

    return combined_summary

def clean_summary(summary):
    result = []
    new_summary = "[" + summary.replace('AI:', '').replace('\n', '').replace('\n\n', '').replace('    ', '').replace('}', '},') + "]"
    extracted_content = re.findall(r'\{(.*?)\}', new_summary, re.DOTALL)

    for content in extracted_content:
        content = "{" + content + "}"
        content = json.loads(content)
        result.append(content)
    return result

def get_summary_and_quiz(document_text, difficulty_level):
    model = ChatOpenAI(model_name="gpt-4")

    # Summarize the document
    beginner_summary = "an easy and simplified style for beginners, focusing on key points and simple language"
    intermediate_summary = "a medium style with moderate detail, providing main ideas and some context"  
    hard_summary = "a hard and detailed style with technical vocabulary and nuanced explanations, suitable for advanced learners"

    # Match the user's choice to a style
    if difficulty_level == 'easy':
        summary = summarize_document(model, document_text, chunk_size=3000, summary_type=beginner_summary)
        quiz = create_quiz(model, summary, mode="easy")
    elif difficulty_level == 'medium':
        summary = summarize_document(model, document_text, chunk_size=2000, summary_type = intermediate_summary)
        quiz = create_quiz(model, summary, mode="medium")
    elif difficulty_level == 'hard':
        summary = summarize_document(model, document_text, chunk_size=1000, summary_type = hard_summary)
        quiz = create_quiz(model, summary, mode="hard")

    return clean_summary(summary), json.loads(quiz)
