import os
import gradio as gr
from dotenv import load_dotenv
from groq import Groq
from embed_retrieve import retrieve, load_vector_store

load_dotenv()

MODEL = "llama-3.3-70b-versatile"
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# load once at startup so the first query isn't slow
collection, model = load_vector_store()


def build_context(chunks):
    # format retrieved chunks into numbered blocks for the prompt
    sections = []
    for i, chunk in enumerate(chunks, start=1):
        meta = chunk["metadata"]
        sections.append(
            f"[{i}] {meta['title']} ({meta['source']})\n{chunk['text']}"
        )
    return "\n\n".join(sections)


def build_sources(chunks):
    # build the sources list from metadata — not from whatever the LLM says
    seen = []
    lines = []
    for chunk in chunks:
        meta = chunk["metadata"]
        key = meta["url"]
        if key not in seen:
            seen.append(key)
            lines.append(f"- {meta['title']} — {meta['source']} — {meta['url']}")
    return "\n".join(lines)


# sends retrieved context + question to Groq with a grounding prompt
def generate(question, chunks):
    context = build_context(chunks)

    prompt = f"""Answer the question using only the information in the provided documents.
If the documents don't contain enough information to answer, say "I don't have enough information on that."
Do not use outside knowledge or speculate beyond what the documents say.

When you state a fact or claim, cite the source inline using the document title in parentheses — for example: "According to First-Year Survival Guide, students recommend getting involved early (source: First-Year Survival Guide)."

Documents:
{context}

Question: {question}"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
    )

    return response.choices[0].message.content.strip()


def answer_question(question):
    if not question.strip():
        return "Please enter a question."

    chunks = retrieve(question, collection=collection, model=model)

    answer = generate(question, chunks)
    sources = build_sources(chunks)

    # return separately so Gradio can put them in two distinct boxes
    return answer, sources


with gr.Blocks(title="Unofficial Amherst Guide") as demo:
    gr.Markdown(
        "## Unofficial Amherst Guide\n"
        "Ask questions about Amherst College academics, dining, social life, and more. "
        "Answers are generated from retrieved student blog posts, Reddit discussions, "
        "and official Amherst sources — not from general AI knowledge."
    )
    inp = gr.Textbox(label="Your question", lines=2, placeholder="Ask anything about Amherst College...")
    btn = gr.Button("Ask")
    answer_box = gr.Textbox(label="Answer", lines=8)
    sources_box = gr.Textbox(label="Retrieved from", lines=4)

    btn.click(answer_question, inputs=inp, outputs=[answer_box, sources_box])
    inp.submit(answer_question, inputs=inp, outputs=[answer_box, sources_box])

if __name__ == "__main__":
    demo.launch()