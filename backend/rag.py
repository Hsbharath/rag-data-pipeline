import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

_MODEL_NAME = "google/flan-t5-base"

# Loaded once at startup — reused across all requests
print(f"Loading RAG generation model: {_MODEL_NAME}")
_tokenizer = AutoTokenizer.from_pretrained(_MODEL_NAME)
_model = AutoModelForSeq2SeqLM.from_pretrained(_MODEL_NAME)
_model.eval()

_MAX_NEW_TOKENS = {"low": 100, "high": 500}


def generate_answer(query: str, chunks: list[dict], detail: str = "high") -> str:
    """
    Generate a natural language answer from retrieved chunks.
    Uses flan-t5-base for local, free inference — no external APIs required.
    detail="low"  → concise answer (~100 tokens)
    detail="high" → detailed answer (~500 tokens)
    """
    max_new_tokens = _MAX_NEW_TOKENS.get(detail, _MAX_NEW_TOKENS["high"])
    context = "\n\n".join(chunk["text"] for chunk in chunks)

    # flan-t5 works best with explicit instruction framing
    if detail == "low":
        instruction = (
            "Answer the following question in one or two short sentences. "
            "Be direct and concise. Do not elaborate."
        )
    else:
        instruction = (
            "Answer the following question in detail. "
            "Provide a thorough, elaborated explanation with multiple sentences."
        )

    prompt = (
        f"{instruction}\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n\n"
        f"Answer:"
    )

    inputs = _tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)

    with torch.no_grad():
        output_ids = _model.generate(**inputs, max_new_tokens=max_new_tokens)

    return _tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()
