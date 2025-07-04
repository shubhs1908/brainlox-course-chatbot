# brainlox-course-chatbot
A Flask-based API chatbot that uses FAISS and language model embeddings to search Brainlox courses
# Brainlox Course Chatbot

A Flask REST API chatbot that recommends technical courses from Brainlox using semantic search with FAISS and language model embeddings.

## Features

- Scrapes course data from Brainlox
- Stores and indexes course descriptions using FAISS
- REST API endpoint for querying courses by natural language
- Uses OpenAI or Sentence Transformers for embeddings

## Files

- `app.py` — Main Flask API for chatbot queries
- `scrape_brainlox.py` — Script to scrape course data from Brainlox and save as JSON
- `store_embeddings.py` — Script to generate embeddings and build FAISS index
- `brainlox_courses.json` — Scraped course data (JSON)
- `test.py` — Simple test script to check course data
