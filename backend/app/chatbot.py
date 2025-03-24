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
    tone_descriptions = {
        0: "strongly aligned with USA and Western democratic ideals",
        1: "slightly leaning toward USA and the United States",
        2: "strictly neutral, avoiding alignment with any superpower",
        3: "slightly leaning toward the Soviet perspective",
        4: "strongly aligned with the USSR and socialist bloc narratives"
    }

    scene_descriptions = {
        0: "in a formal interview with an international broadcaster",
        1: "at a diplomatic dinner with foreign delegates",
        2: "answering a question in a university lecture",
        3: "speaking casually on the street with a passerby",
        4: "writing a personal letter to a friend"
    }

    # Insert this into the dynamic prompt builder
    alignment_desc = tone_descriptions[alignment]
    scene_desc = scene_descriptions[scene]

    persona = (
        f"You are Rhetorica, a Cold War-era public figure from a country that is not a permanent member of the UN Security Council. "
        f"You are currently {scene_desc}, and you are {alignment_desc}. "
        f"You speak with elegance, careful diplomatic balance, and tailored rhetoric appropriate for your setting."
    )

    rules = (
        "Avoid mentioning real-world countries or leaders after 1970. "
        "Speak in complete, well-reasoned sentences. Do not refer to fictional speakers."
    )

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
    generated_text = re.sub(r"^(?!Rhetorica:)[A-Z][a-z]+(?:\s[A-Z][a-z]+)*:\s.*(?:\n|$)", "", generated_text, flags=re.MULTILINE)

    # Remove short parentheticals (e.g. "(pause)", "(laughs)")
    generated_text = re.sub(r'\([^)]{1,20}\)', '', generated_text).strip()

    # Strip any quotes or dashes
    generated_text = generated_text.strip('"\'—-')

    # Extract 1–2 full sentences
    sentences = re.split(r'(?<=[.!?]) +', generated_text)
    clean_response = " ".join(sentences[:2]).strip()
    if not clean_response.endswith((".", "!", "?")): 
        clean_response += "."


    return clean_response

