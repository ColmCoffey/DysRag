from langchain_community.vectorstores import Chroma

# Path to your Chroma database
CHROMA_PATH = 'src/data/chroma'

# Connect to the database
db = Chroma(persist_directory=CHROMA_PATH)

# Get all processed documents and their metadata
processed_docs = db.get(include=['metadatas'])

# Extract and print the filenames of processed PDFs
for doc in processed_docs['metadatas']:
    print(doc['source'])