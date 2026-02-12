#  This module will serve as the main entry point for the application, handling tasks related to deploying and interacting with the trained model

# Flask is a lightweight and powerful web framework for Python.
# It’s often called a "micro-framework" because it provides the essentials for web development without unnecessary complexity
# render_template will help us render the html template in frontend folder
from flask import Flask, render_template, request, Response, jsonify

# Prometheus is open source monitoring system for Kubernetes used to collect and store real-time metrics (like CPU usage,memory,request)
# for a application running in Kubernetes. We can also make custom metrics in Prometheus
# Counter below is used to count the number of requests we are getting.
from prometheus_client import Counter, generate_latest
import uuid

from flipkart.data_ingestion import DataIngestor
from flipkart.rag_agent import RAGAgentBuilder

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Prometheus metrics - counting the number of requests and predictions we make
REQUEST_COUNT = Counter("http_requests_total","Total HTTP Requests")
PREDICTION_COUNT = Counter("model_predictions_total","Total Model Predictions")

# Creating an application
def create_app():
    # Initating app using template(index.html) and styling(style.css) files
    app = Flask(__name__,template_folder="frontend/templates",static_folder="frontend/static")

    # Create a new thread for every app run. Everytime we refresh, a new uuid(universal unique id) will be
    # assigned. This is useful for creating session memory
    THREAD_ID = str(uuid.uuid4())
    print(f"[INFO] New chat thread created: {THREAD_ID}")

    # Load/ingest vector store if not done already
    vector_store = DataIngestor().ingest(load_existing=True)

    # Build RAG Agent (Langchain + Langgraph)
    rag_agent = RAGAgentBuilder(vector_store).build_agent()

    # Using @app.route, we can easily map URLs to functions, making code more readable and structured.
    # Flask allows dynamic URL handling, making it easy to pass parameters in routes
    @app.route("/")
    def index():
        REQUEST_COUNT.inc()
        return render_template("index.html")
    
    # When we hit enter button to fire the query, we're going to fetch a response
    @app.route("/get", methods=["POST"])
    def get_response():
        REQUEST_COUNT.inc()

        user_input = request.form["msg"]

        # Invoke agent with LangGraph thread-based memory
        # This is how we invoke/provide messages to LLM
        response = rag_agent.invoke(
            {
                "messages":[
                    {
                        "role": "user", # Role is user since we are providing the message
                        "content": user_input
                    }
                ]
            },
            config = {
            "configurable": { # We're maintaining a configurable thread_id as we want to maintain session memory and chat history
                "thread_id": THREAD_ID
                }
            }
        )

        # Counting our prediction count
        PREDICTION_COUNT.inc()

        if not response.get("messages"):
            return "Sorry, I couldn't find any product information relevant to your query"
        
        # Return latest assistant message
        return response["messages"][-1].content
    
    # We have a health route - If everything is working fine, we write 200 (standard metric)
    @app.route("/health")
    def health():
        return jsonify({"status":"healthy"}), 200
    
    # We are also going to route metrics which will help us with the Prometheus part
    @app.route("/metrics")
    def metrics():
        return Response(generate_latest(),mimetype="text/plain")
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0",port=5000,debug=True)











