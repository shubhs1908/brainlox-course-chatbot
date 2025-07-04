from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import faiss
import numpy as np
from langchain.embeddings.openai import OpenAIEmbeddings
import json

app = Flask(__name__)
api = Api(app)

# Load FAISS Index
faiss_index = faiss.read_index("brainlox_faiss.index")

# Load Scraped Data
with open("brainlox_courses.json", "r") as f:
    course_data = json.load(f)

# Initialize OpenAI Embeddings
embedding_model = OpenAIEmbeddings(openai_api_key="your-openai-api-key")

# Define API Resource
class Chatbot(Resource):
    def post(self):
        try:
            # Get user query
            query = request.json["query"]
            
            # Convert query to embedding
            query_embedding = np.array([embedding_model.embed_query(query)], dtype="float32")

            # Search in FAISS
            _, result_indices = faiss_index.search(query_embedding, k=3)

            # Retrieve top results
            results = [course_data[i] for i in result_indices[0]]

            return jsonify({"response": results})

        except Exception as e:
            return jsonify({"error": str(e)})

# Add Resource
api.add_resource(Chatbot, "/chat")

if __name__ == "__main__":
    app.run(debug=True)