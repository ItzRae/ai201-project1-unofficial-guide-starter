"""
Milestone 3 — Document Ingestion & Chunking
Amherst College Unofficial Guide RAG Pipeline

Loads .txt files from the /documents folder, cleans text, and produces
chunks of 600–800 characters with ~100 characters of overlap.

Expected .txt file header format:
    Title: A College Kid's Guide to Amherst
    Source: College Kid Guide
    URL: https://www.collegekidguide.com/...

    (Text) Because Amherst Coll...
"""

import os
import re
import json

# ── Config ────────────────────────────────────────────────────────────────────
DOCUMENTS_DIR = "documents"          # folder containing your .txt files
OUTPUT_FILE   = "chunks.json"        # where chunks are saved
CHUNK_SIZE    = 700                  # target chars (600–800 window)
CHUNK_OVERLAP = 100                  # overlap chars between consecutive chunks
# ─────────────────────────────────────────────────────────────────────────────


def parse_document(filepath: str) -> dict:
    """
    Parses a .txt file with the header format:
        Title: ...
        Source: ...
        URL: ...

        (Text) body...

    Returns a dict with keys: title, source, url, body.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    metadata = {"title": "", "source": "", "url": ""}
    body = raw

    # Extract header lines (Title / Source / URL) from the top of the file
    header_pattern = re.compile(
        r"^Title:\s*(?P<title>.+?)\n"
        r"Source:\s*(?P<source>.+?)\n"
        r"URL:\s*(?P<url>\S+)",
        re.IGNORECASE | re.MULTILINE,
    )
    m = header_pattern.search(raw)
    if m:
        metadata["title"]  = m.group("title").strip()
        metadata["source"] = m.group("source").strip()
        metadata["url"]    = m.group("url").strip()
        # Body starts after the header block
        body = raw[m.end():]

    # Strip the optional "(Text)" marker
    body = re.sub(r"^\s*\(Text\)\s*", "", body, flags=re.IGNORECASE).strip()

    return {**metadata, "body": body}


def clean_text(text: str) -> str:
    """
    Light cleaning:
    - Collapse multiple blank lines to a single newline
    - Collapse runs of whitespace (spaces/tabs) to a single space
    - Strip leading/trailing whitespace
    """
    text = re.sub(r"\r\n", "\n", text)          # normalise line endings
    text = re.sub(r"[ \t]+", " ", text)         # collapse inline whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)      # max two consecutive newlines
    text = text.strip()
    return text


def chunk_text(text, chunk_size=750, overlap=100):
    paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 0]

    chunks = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) + 2 <= chunk_size:
            current += ("\n\n" if current else "") + para
        else:
            if len(current.strip()) >= 300:
                chunks.append(current.strip())

            current = para

            while len(current) > chunk_size:
                split_at = current.rfind(". ", 0, chunk_size)
                if split_at == -1:
                    split_at = current.rfind(" ", 0, chunk_size)
                if split_at == -1:
                    split_at = chunk_size

                piece = current[:split_at + 1].strip()
                if len(piece) >= 300:
                    chunks.append(piece)

                remaining = current[split_at + 1:].strip()

                # overlap from the end of previous piece, but start at a word boundary
                overlap_text = piece[-overlap:].strip()
                first_space = overlap_text.find(" ")
                if first_space != -1:
                    overlap_text = overlap_text[first_space + 1:]

                current = (overlap_text + " " + remaining).strip()

    if len(current.strip()) >= 300:
        chunks.append(current.strip())

    return chunks


def process_all_documents(documents_dir: str) -> list[dict]:
    """
    Reads every .txt file in *documents_dir*, cleans the body, chunks it,
    and returns a flat list of chunk dicts ready for embedding.
    """
    all_chunks = []
    txt_files  = sorted(
        f for f in os.listdir(documents_dir) if f.endswith(".txt")
    )

    if not txt_files:
        print(f"[WARNING] No .txt files found in '{documents_dir}'.")
        return all_chunks

    for filename in txt_files:
        filepath = os.path.join(documents_dir, filename)
        print(f"Processing: {filename}")

        doc    = parse_document(filepath)
        clean  = clean_text(doc["body"])
        chunks = chunk_text(clean)

        for i, chunk_text_content in enumerate(chunks):
            all_chunks.append({
                "chunk_index": i,
                "source_file": filename,
                "title":       doc["title"],
                "source":      doc["source"],
                "url":         doc["url"],
                "text":        chunk_text_content,
                "char_count":  len(chunk_text_content),
            })

        print(f"  → {len(chunks)} chunks  (avg {sum(len(c) for c in chunks)//max(len(chunks),1)} chars each)")

    return all_chunks


def print_sample(chunks: list[dict], n: int = 5) -> None:
    """Print the first *n* chunks for quick visual verification."""
    print("\n" + "═" * 70)
    print(f"SAMPLE OUTPUT — first {n} chunks")
    print("═" * 70)
    for chunk in chunks[:n]:
        print(f"\nFile      : {chunk['source_file']}")
        print(f"Title     : {chunk['title']}")
        print(f"Source    : {chunk['source']}")
        print(f"URL       : {chunk['url']}")
        print(f"Chunk idx : {chunk['chunk_index']}")
        print(f"Char count: {chunk['char_count']}")
        print(f"Text      : {chunk['text'][:500]}{'...' if len(chunk['text']) > 200 else ''}")
        print("-" * 70)


def main():
    if not os.path.isdir(DOCUMENTS_DIR):
        raise FileNotFoundError(
            f"Documents folder '{DOCUMENTS_DIR}' not found. "
            "Create it and add your .txt files there."
        )

    chunks = process_all_documents(DOCUMENTS_DIR)

    # Save to JSON for use in Milestone 4
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"\n✓ {len(chunks)} total chunks saved to '{OUTPUT_FILE}'")

    print_sample(chunks)

    # Quick stats
    if chunks:
        sizes = [c["char_count"] for c in chunks]
        print(f"\nChunk size stats:")
        print(f"  Min : {min(sizes)} chars")
        print(f"  Max : {max(sizes)} chars")
        print(f"  Avg : {sum(sizes)//len(sizes)} chars")
        out_of_range = [s for s in sizes if not (500 <= s <= 900)]
        if out_of_range:
            print(f"  ⚠ {len(out_of_range)} chunks slightly outside 500–900 char range (boundary fragments)")
        else:
            print("  ✓ All chunks within expected size range")


if __name__ == "__main__":
    main()