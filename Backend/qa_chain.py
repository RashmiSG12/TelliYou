from langchain.chains import RetrievalQA
# from langchain_openai import ChatOpenAI
import os
from Backend.prompt import prompts
import google.generativeai as genai
from Backend.gemini import GeminiLLM

def load_llm():
    llm = GeminiLLM()
    return llm



def create_qa_chain(llm, retriever):
    qa_chain = RetrievalQA.from_chain_type(llm=llm, 
                                           retriever=retriever,
                                           chain_type = "stuff",
                                           chain_type_kwargs = {"prompt": prompts()})
    return qa_chain