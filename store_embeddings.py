from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json
import os

app = Flask(__name__)
api = Api(app)

# Path to FAISS index and JSON file
FAISS_INDEX_PATH = "brainlox_faiss.index"
COURSE_DATA_PATH = "brainlox_courses.json"

# Load Scraped Data
if os.path.exists(COURSE_DATA_PATH):
    with open(COURSE_DATA_PATH, "r") as f:
        course_data = json.load(f)
else:
    raise FileNotFoundError(f"Error: {COURSE_DATA_PATH} not found!")

# Initialize Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Function to rebuild FAISS index if needed
def build_faiss_index():
    print("[INFO] Building FAISS index...")
    
    # Convert all course descriptions into embeddings
    embeddings = np.array(
        [model.encode(course["content"], normalize_embeddings=True) for course in course_data], dtype="float32"
    )

    # Create FAISS index
    faiss_index = faiss.IndexFlatL2(embeddings.shape[1])
    faiss_index.add(embeddings)  # Add embeddings to FAISS index

    # Save FAISS index
    faiss.write_index(faiss_index, FAISS_INDEX_PATH)
    print(f"[SUCCESS] FAISS Index built with {faiss_index.ntotal} entries!")

# Check if FAISS index exists, else create it
if not os.path.exists(FAISS_INDEX_PATH):
    build_faiss_index()

# Load FAISS Index
faiss_index = faiss.read_index(FAISS_INDEX_PATH)
print(f"[INFO] FAISS Index contains {faiss_index.ntotal} vectors.")

# Define API Resource
class Chatbot(Resource):
    def post(self):
        try:
            # Get user query
            query = request.json.get("query", "").strip()
            if not query:
                return jsonify({"error": "Query cannot be empty!"})

            # Convert query to embedding
            query_embedding = np.array([model.encode(query, normalize_embeddings=True)], dtype="float32")

            # Search in FAISS
            _, result_indices = faiss_index.search(query_embedding, k=3)

            # Retrieve top results
            results = [course_data[i] for i in result_indices[0] if i < len(course_data)]

            return jsonify({"response": results})

        except Exception as e:
            return jsonify({"error": str(e)})

# Add Resource
api.add_resource(Chatbot, "/chat")

if __name__ == "__main__":
    app.run(debug=True)