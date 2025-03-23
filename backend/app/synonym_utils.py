import spacy
from sentence_transformers import SentenceTransformer, util

# Load spaCy model for lemmatization
nlp = spacy.load("en_core_web_md")

# Load SBERT model
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_dynamic_threshold(word):
    """Further relaxes the similarity threshold to allow more synonyms."""
    base_threshold = 0.6  # Lowered to allow near-misses
    return max(0.45, base_threshold - (len(word) * 0.015))  # More flexible range

def get_sbert_synonyms(word, response_keys):
    """Finds synonyms using SBERT and a dynamic threshold, sorted by relevance."""
    synonyms = []
    context_sentence = f"{word} as a concept"
    word_embedding = sbert_model.encode(context_sentence, convert_to_tensor=True)
    threshold = get_dynamic_threshold(word)

    for candidate in response_keys:
        candidate_sentence = f"{candidate} in relation to ideas"
        candidate_embedding = sbert_model.encode(candidate_sentence, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(word_embedding, candidate_embedding).item()

        boost_factor = 1 + (0.08 if similarity > (threshold - 0.07) else 0)
        adjusted_similarity = similarity * boost_factor

        if adjusted_similarity > threshold:
            synonyms.append((candidate, adjusted_similarity))

    synonyms.sort(key=lambda x: x[1], reverse=True)
    return [syn[0] for syn in synonyms[:3]]
