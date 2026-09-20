"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

from dataclasses import dataclass
import re

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split the city-guide documents into paragraph-aware chunks.

    Chunks have a 400-character maximum and no overlap. Headings stay with
    the content they introduce when possible, and oversized blocks are split
    at word boundaries.
    """
    max_chars = 400
    # Store every chunk created from every source document.
    chunks: list[Chunk] = []

    for doc in documents:
        # Split each Markdown document at blank lines so paragraphs and
        # headings become separate blocks instead of fixed-size fragments.
        raw_blocks = [
            block.strip()
            for block in re.split(r"\n\s*\n", doc.text)
            if block.strip()
        ]

        # Keep each heading with the content it introduces. This prevents a
        # heading from being stranded at the end of the previous chunk.
        blocks: list[str] = []
        position = 0
        while position < len(raw_blocks):
            block = raw_blocks[position]
            if (
                re.match(r"^#{1,6}\s", block)
                and position + 1 < len(raw_blocks)
            ):
                blocks.append(block + "\n\n" + raw_blocks[position + 1])
                position += 2
            else:
                blocks.append(block)
                position += 1

        # Build one output chunk by combining complete blocks until adding
        # another block would exceed the character limit.
        current: list[str] = []
        current_length = 0
        index = 0

        def emit(piece: str) -> None:
            # Convert finished text into the Chunk object expected by the
            # rest of the retrieval pipeline.
            nonlocal index
            piece = piece.strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::split_documents",
                    )
                )
                index += 1

        for block in blocks:
            # If one block is too long, flush the current chunk and split the
            # oversized block at word boundaries rather than cutting a word.
            if len(block) > max_chars:
                if current:
                    emit("\n\n".join(current))
                    current = []
                    current_length = 0

                words: list[str] = []
                word_length = 0
                for word in block.split():
                    added_length = len(word) if not words else len(word) + 1
                    if words and word_length + added_length > max_chars:
                        emit(" ".join(words))
                        words = [word]
                        word_length = len(word)
                    else:
                        words.append(word)
                        word_length += added_length
                if words:
                    emit(" ".join(words))
                continue

            # Count the blank line that will separate this block from the
            # previous one when deciding whether it fits in the current chunk.
            added_length = len(block) if not current else len(block) + 2
            if current and current_length + added_length > max_chars:
                # Save the full current chunk before starting a new one.
                emit("\n\n".join(current))
                current = []
                current_length = 0

            # Add this complete block to the chunk currently being assembled.
            current.append(block)
            current_length += len(block) if len(current) == 1 else len(block) + 2

        if current:
            # Save the final partial chunk from this document.
            emit("\n\n".join(current))

    # Return all chunks so indexing and retrieval can use them.
    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
