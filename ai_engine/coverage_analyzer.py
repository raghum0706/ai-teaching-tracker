import re
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def analyze_coverage(topics, lecture_path):
    with open(lecture_path, "r", encoding="utf-8", errors="ignore") as f:
        lecture_text = f.read().lower()

    # Split transcript into chunks (every 3-4 sentences) to find specific mentions
    sentences = re.split(r'[.!?]', lecture_text)
    chunks = [" ".join(sentences[i:i+3]) for i in range(0, len(sentences), 3)]
    
    if not chunks: chunks = [lecture_text]
    
    lecture_embeddings = model.encode(chunks, convert_to_tensor=True)
    results = {}

    for topic in topics:
        clean_topic = topic.lower()
        topic_embedding = model.encode(clean_topic, convert_to_tensor=True)

        # 1. Semantic Check: Find the highest similarity in any part of the transcript
        cos_scores = util.cos_sim(topic_embedding, lecture_embeddings)
        semantic_score = float(cos_scores.max().item()) * 100

        # 2. Keyword Check: Does the exact topic name appear?
        keyword_present = 100 if clean_topic in lecture_text else 0

        # Final score: 70% Semantic + 30% Keyword boost
        final_coverage = round((semantic_score * 0.7) + (keyword_present * 0.3), 2)

        if final_coverage >= 55:
            status = "Completed"
        elif 30 <= final_coverage < 55:
            status = "Partially Covered"
        else:
            status = "Not Completed"

        results[topic] = (final_coverage, status)

    return results
