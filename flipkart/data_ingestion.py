# This module initializes the AstraDB Vector Store, converts the csv file -->documents-->HuggingFaceEmbdeddings and stores them in AstraDB Vector store  

from langchain_astradb import AstraDBVectorStore # required to access AstraDB Vector Store
from langchain_huggingface import HuggingFaceEmbeddings # required to convert docs to embeddings
# Modular coding being used in below lines
from flipkart.config import Config
from flipkart.data_converter import DataConverter

class DataIngestor:
    def __init__(self):
        self.embedding = HuggingFaceEmbeddings(model = Config.EMBEDDING_MODEL)

        # Initilizing astraDB Vector Store
        self.vstore = AstraDBVectorStore(
            embedding = self.embedding,
            collection_name ='flipkart',
            api_endpoint = Config.ASTRA_DB_API_ENDPOINT,
            token = Config.ASTRA_DB_APPLICATION_TOKEN,
            namespace = Config.ASTRA_DB_KEYSPACE
        )

# load_exisiting parameter - if docs already exists just load that 
    def ingest(self,load_existing = True):
        if load_existing == True:
            return self.vstore
        
        docs = DataConverter("data/flipkart_headphones_reviews_dataset_full.csv").convert()

        self.vstore.add_documents(docs)

        return self.vstore

if __name__ == "__main__":
    ingestor = DataIngestor()
    ingestor.ingest(load_existing=False)


