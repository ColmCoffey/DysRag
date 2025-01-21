# Cervical Dystonia RAG System Architecture

## Introduction
This project implements a RAG (Retrieval Augmented Generation) system that processes medical literature about Cervical Dystonia, a neurological movement disorder characterized by painful, involuntary neck muscle contractions and abnormal head positioning. Deployed as a serverless application on AWS, it provides accurate, citation-backed responses through a cost-effective architecture (approximately $0.002 per query). The system serves as a specialized knowledge base for healthcare providers and researchers, enabling efficient access to evidence-based information about symptoms, treatments, and research developments.

## Architecture
![DepRag_architecture](https://github.com/user-attachments/assets/97d1c12f-a503-4513-8df8-9cd20788df69)

The system provides a cost effective and scalable solution for deploying a medical knowledge base with modern RAG capabilities, specifically focused on Cervical Dystonia information retrieval and analysis. Its serverless architecture ensures cost-effective scaling while maintaining reliable performance for medical information queries.

### 1. Data Processing Layer
* **STORAGE**: ChromaDB as vector database
* **CHUNKING**: LangChain's RecursiveCharacterTextSplitter with:
  * Chunk size: 600 characters
  * Chunk overlap: 120 characters
* **EMBEDDINGS**: AWS Bedrock generates embeddings
* **DATA STRUCTURE**: Document chunks include metadata (source:page:chunk_index)

### 2. API Layer (FastAPI)
```python
Endpoints:
/submit_query (POST)
- Accepts query text
- Returns query_id immediately
- Triggers asynchronous processing

/get_query (GET)
- Accepts query_id
- Returns completed response or processing status
```

### 3. Serverless Infrastructure
* **COMPUTE**: AWS Lambda with containerized deployment
  * API Function: 256MB memory, 30-second timeout
  * Worker Function: Higher memory/timeout for processing
* **DATABASE**:
  * DynamoDB table with query_id as partition key
  * Pay-per-request billing model
* **CONTAINER**:
  * AWS Lambda Python 3.11 base image
  * Required dependencies installed via requirements.txt
  * SQLite modifications for ChromaDB compatibility

### 4. Query Processing Flow
```
User Query → API Lambda → DynamoDB (initial entry)
                      ↓
         Async Worker Lambda (processing)
                      ↓
         1. Retrieve relevant chunks
         2. Generate embedding
         3. Search vector database
         4. Construct prompt with context
         5. Get LLM response
                      ↓
         DynamoDB (update with response)
                      ↓
User polls → API Lambda → DynamoDB (fetch result)
```

### 5. Infrastructure as Code (AWS CDK)
```
Components:
- DynamoDB table definition
- Lambda function configurations
- IAM roles and permissions
- Function URL setup
```

### 6. Security & Permissions
* API function: DynamoDB access
* Worker function: 
  * DynamoDB access
  * Bedrock access
* Public function URLs without authentication

### 7. Cost Structure
* Approximately 2 euro per 1000 requests
* Pay-per-use model for all components:
  * Lambda invocations
  * DynamoDB operations
  * Bedrock API calls

## Technical Implementation Details

### 1. Docker Container Build
* Base image: public.ecr.aws/lambda/python:3.11
* Custom SQLite installation for ChromaDB compatibility
* Environment variable setup for runtime detection
* Source code and database file copying

### 2. FastAPI Implementation
* Mangum adapter for Lambda compatibility
* Asynchronous endpoint design
* Error handling for response types

### 3. Database Operations
* Initial ChromaDB setup for vector storage
* DynamoDB for query tracking
* Efficient data retrieval patterns

