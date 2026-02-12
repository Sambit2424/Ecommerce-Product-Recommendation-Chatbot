# This module creates classes to build prediction pipeline using the data ingested in AstraDB Vector store

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware # here middleware refers to our chat history with LLM. Since LLM hallucinates after 15-20 prompts,multiple messages are summarized into one message with help of this clss to preserve chat context w.r.t history 
from langgraph.checkpoint.memory import InMemorySaver # Maintain chat history
from langchain.tools import tool # Astradb acts a retrieval tool which will help us to fetch documents relevant to flipkart
from flipkart.config import Config

def build_flipkart_retriever_tool(retriever):

    @tool
    def flipkart_retriever_tool(query:str) -> str:
         # Function will only take string as input and generate output as string
         """
         Retrieve top product reviews related to the user query
         """

         docs = retriever.invoke(query)
         return "\n\n".join(doc.page_content for doc in docs)
    
    return flipkart_retriever_tool


class RAGAgentBuilder:
    def __init__(self,vector_store):
        #  This function takes two parameters - the Astradb vector store we built and the qwen(from groq cloud) RAG_model we specified in config file
        self.vector_store = vector_store
        self.model = init_chat_model(Config.RAG_MODEL)
          
    def build_agent(self):
        # Converting the AstrDB Vector Store as retriever and fetching the top 3 relevant documents
        retriever = self.vector_store.as_retriever(search_kwargs={"k":3})
        # Converting retriever into a flipkart retriever tool
        flipkart_tool = build_flipkart_retriever_tool(retriever)


        agent = create_agent(
            model = self.model,
            tools = [flipkart_tool],
            system_prompt="""

            You're a chatbot for ecommerce platform who answers product-related queries
            based on their titles and reviews.

            To find the answers to any query, always use flipkart_retriever_tool.

            If you do not know an answer, politely say that I don't know the answer,
            please contact our customer care at +91 0707076666 or drop mail at
            customer_care@bigecom.com 

            """,
            # Below code is for maintaining memory and preserving context w.r.t chat history 
            checkpointer = InMemorySaver(),
            middleware=[
                SummarizationMiddleware(
                model = self.model,
                trigger=("messages",10),
                keep = ("messages",4)
                )
            ],
        )

        return agent
    
     

