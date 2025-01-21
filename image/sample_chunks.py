from langchain_community.vectorstores import Chroma
import random

# Save this as "sample_chunks.py" in your working directory
CHROMA_PATH = 'src/data/chroma'
db = Chroma(persist_directory=CHROMA_PATH)

# Get all documents and metadata 
docs = db.get(include=['documents', 'metadatas'])

# Get total number of chunks
total_chunks = len(docs['documents'])

# Sample 20 random chunks
sample_indices = random.sample(range(total_chunks), 20)

# Open file to write
with open('randomly_selected_chunks.txt', 'w', encoding='utf-8') as f:
    for idx in sample_indices:
        f.write(f"\n{'='*80}\n")
        f.write(f"Chunk {idx} from {docs['metadatas'][idx]['source']}\n")
        f.write(f"{'='*80}\n\n")
        f.write(docs['documents'][idx])
        f.write('\n\n')

print("Chunks have been saved to 'randomly_selected_chunks.txt'")