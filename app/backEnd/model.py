from youtube_transcript_api import YouTubeTranscriptApi
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM
from torch import amp


def get_transcript(video_url):
    # Extract video ID from URL
    if 'v=' in video_url:
        video_id = video_url.split('v=')[1].split('&')[0]
    else:
        raise ValueError("Invalid YouTube URL")

    # Fetch transcript
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US','ar'])

    # Combine into one text block
    full_text = ' '.join([entry['text'] for entry in transcript])

    return full_text


def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(text)
    return chunks


embedder = SentenceTransformer('all-MiniLM-L6-v2')

def embed_chunks(chunks):
    embeddings = embedder.encode(chunks)
    return embeddings


def create_faiss_index(embeddings):
    embeddings = np.array(embeddings).astype('float32')
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index


def retrieve_relevant_chunks(question, chunks, index, top_k=4):
    # Embed question
    question_embedding = embedder.encode([question]).astype('float32')

    # Search in FAISS
    D, I = index.search(question_embedding, top_k)

    # Get top_k chunks
    retrieved_chunks = [chunks[i] for i in I[0]]
    return retrieved_chunks



model_name = "TheBloke/Mistral-7B-Instruct-v0.2-GPTQ"


tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    trust_remote_code=True,
    revision="main"
)


def generateAnswer(url,question):
    try:
        transcript_text = get_transcript(url)
        chunks = chunk_text(transcript_text)
        print(f"Number of chunks: {len(chunks)}")
        
        embeddings = embed_chunks(chunks)
        print(f"Embeddings shape: {embeddings.shape}")
        
        index = create_faiss_index(embeddings)
        print(f"FAISS index created with {index.ntotal} vectors.")
        
        # Retrieve relevant chunks
        results = retrieve_relevant_chunks(question, chunks, index)
        print("\nRetrieved Context:")
        for i, chunk in enumerate(results):
            print(f"Chunk {i+1}:\n{chunk}\n")
        
        # Create prompt by combining question + retrieved context
        context = "\n\n".join(results)
        prompt = f"""
        You are a helpful assistant. Use ONLY the provided context to answer the question.
        Keep your answer clear, short, and direct.

        Context: {context}

        Question: {question}

        gptqAnswer:

        """


        
        # Tokenize prompt
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        model.eval()

        # Generate output 
        with amp.autocast('cuda'):
            outputs = model.generate(
                **inputs,
                max_new_tokens=50,
                do_sample=False,
                temperature=0.7,
                top_p=0.9
            )
        
        # Decode and print answer
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        if "gptqAnswer:" in answer:
            # Split by 'Answer:' and take the last part
            return answer.split("Answer:")[-1].strip()
        else:
            # If no 'Answer:' found, return the full output trimmed
            return answer.strip()


        
    except Exception as e:
        print(f"Error: {e}")


