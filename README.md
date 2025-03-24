# Rhetorica-Bot
# 🌐 Rhetorica Bot

A Cold War–era LLM-powered chatbot that simulates diplomatic rhetoric across political alignments and conversational settings.

## 🎯 What It Does

Rhetorica Bot responds to user questions in the voice of a Cold War-era public figure from a fictional non-permanent member state of the UN Security Council. Responses are generated dynamically and shaped by two dimensions:

- **Political Alignment:** Pro-USA, Slightly Pro-USA, Neutral (NAM), Slightly Pro-USSR, Pro-USSR
- **Scene Context:** Interview, Diplomatic Dinner, Classroom, Street Conversation, Private Letter

## 🧠 How It Works

- **Backend:** Python + Flask, using TinyLlama via Hugging Face Transformers.
- **Frontend:** React (simple UI with alignment/context sliders + chat window).
- **Prompt Engineering:** Dynamically composes a persona and style prompt based on user input.
- **Output Filtering:** Truncates incomplete answers, removes hallucinated speaker tags, and ensures stylistic tone fidelity.

## 🔍 Example Use Case

> **Question:** What is your view on international diplomacy?  
> *(Alignment: Slightly Pro-USSR, Context: Diplomatic Dinner)*  
>  
> **Response:**  
> *“Diplomacy, when approached with mutual respect and shared interest, becomes a tool not of subjugation, but of solidarity. It is through dialogue—not dominance—that nations grow closer.”*

## 🛠 Features

- Prompt-based rhetorical style simulation
- Inline system messages for scene/alignment changes
- Dynamic prompt construction
- Post-processing for hallucination reduction
- Full-stack GitHub project for demo or portfolio

## 🚧 Known Limitations

- Occasionally truncates longer answers
- Hallucinated roles may appear under extreme prompts
- Model output quality varies with prompt complexity (TinyLlama is intentionally lightweight)
