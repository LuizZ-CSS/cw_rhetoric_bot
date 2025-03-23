import torch
import re
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from app.config import MODEL_PATH

model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH, 
    torch_dtype=torch.float32, 
    low_cpu_mem_usage=True
).to("cpu")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

llama_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=120,  # or up to 150 if you want longer thoughts
    truncation=True,
    pad_token_id=tokenizer.eos_token_id,
    do_sample=True,
    top_k=40,
    top_p=0.9,
    temperature=0.6,
    num_return_sequences=1
)

def generate_response(user_query, alignment=2, scene=0):
    """Generates a response using TinyLlama model."""
    base_intro = (
        "You are a Cold War-era public figure from a fictional Southeast Asian country. "
        "You are articulate and thoughtful, giving a televised interview."
    )

    alignment_personas = {
        0: "You strongly advocate for NATO and Western democratic values, emphasizing collective defense and liberal democracy.",
        1: "You express moderate support for the United States and its democratic ideals, while maintaining some independence.",
        2: "You maintain a balanced, neutral stance, promoting peace and non-alignment in global affairs.",
        3: "You show moderate sympathy for the Soviet Union and socialist ideals, while keeping some distance.",
        4: "You strongly align with the Soviet Union, advocating for socialist revolution and anti-imperialist struggle."
    }

    scene_styles = {
        0: "You speak as if you're giving a formal televised interview, maintaining a professional and measured tone.",
        1: "You speak warmly and tactfully in a formal diplomatic setting, balancing courtesy with political substance.",
        2: "You adopt a clear, structured tone as if explaining complex political concepts to students.",
        3: "You respond naturally and passionately, as if speaking to ordinary citizens on the street.",
        4: "You express yourself sincerely and personally, as if writing a private letter to a trusted confidant."
    }

    rules = (
        "Avoid mentioning real-world countries or leaders after 1970. "
        "Speak in complete, well-reasoned sentences. Do not refer to fictional speakers."
    )
    persona = base_intro + " " + alignment_personas.get(alignment, alignment_personas[2]) + " " + scene_styles.get(scene, scene_styles[0])
    prompt = f"{persona}\n{rules}\n\nQuestion: {user_query}\nAnswer:"
    
    response = llama_pipeline(prompt)
    if not response or len(response) == 0:
        return "I am pondering upon that. Ask me something else."

    generated_text = response[0]["generated_text"].strip()
    
    # Remove the original prompt
    generated_text = generated_text.replace(prompt, "").strip()
    if "Answer:" in generated_text:
        generated_text = generated_text.split("Answer:")[1].strip()

    # Remove hallucinated speaker tags (dynamic, regex-based)
    generated_text = re.sub(r"\b(?!Rhetorica)[A-Z][a-z]+:\s*", "", generated_text)

    # Remove short parentheticals (e.g. "(pause)", "(laughs)")
    generated_text = re.sub(r'\([^)]{1,20}\)', '', generated_text).strip()

    # Strip any quotes or dashes
    generated_text = generated_text.strip('"\'—-')

    # Extract 1–2 full sentences
    sentences = re.split(r'(?<=[.!?]) +', generated_text)
    clean_response = " ".join(sentences[:2]).strip()

    return clean_response

