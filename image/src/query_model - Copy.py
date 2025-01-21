from dataclasses import dataclass
from typing import List
from langchain.prompts import ChatPromptTemplate
from langchain_aws import ChatBedrock
from rag_app.get_chroma_db import get_chroma_db
import sys

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

BEDROCK_MODEL_ID = "amazon.titan-text-lite-v1"

@dataclass
class QueryResponse:
    query_text: str
    response_text: str
    sources: List[str]

def query_rag(query_text: str) -> QueryResponse:
    try:
        print("Initializing Chroma DB...")
        db = get_chroma_db()

        print("Searching database...")
        # Search the DB.
        results = db.similarity_search_with_score(query_text, k=3)
        print(f"Found {len(results)} results")

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)
        print("\nSending to Bedrock...")

        model = ChatBedrock(model_id=BEDROCK_MODEL_ID)
        response = model.invoke(prompt)
        response_text = response.content

        sources = [doc.metadata.get("id", None) for doc, _score in results]
        print(f"\nResponse received from Bedrock")
        print(f"Response: {response_text}\nSources: {sources}")

        return QueryResponse(
            query_text=query_text, response_text=response_text, sources=sources
        )
    except Exception as e:
        print(f"Error occurred: {str(e)}", file=sys.stderr)
        raise

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a query string")
        sys.exit(1)
    
    query_text = sys.argv[1]
    print(f"Processing query: {query_text}")
    query_rag(query_text)