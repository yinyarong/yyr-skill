"""
Clean a YouTube VTT caption file into plain readable prose.

Usage:
    python clean_vtt.py <input.vtt> [output.txt]

If output path is omitted, prints to stdout.

YouTube auto-generated VTT has three kinds of noise this script removes:
  1. The WEBVTT header and per-cue metadata lines (timestamps, position tags)
  2. Inline word-timing tags like <00:00:01.200><c> and </c>
  3. Duplicate lines — YouTube repeats the previous caption text on every new
     cue so words appear to "roll in". We deduplicate by only keeping the
     last version of each repeated prefix.
"""

import re
import sys
from pathlib import Path


def clean_vtt(vtt_text: str) -> str:
    lines = vtt_text.splitlines()

    # Strip the WEBVTT header block and any NOTE/STYLE blocks
    content_lines = []
    skip_block = True
    for line in lines:
        if skip_block:
            # The header ends at the first blank line after "WEBVTT"
            if line.strip() == "" and content_lines == []:
                skip_block = False
            continue
        content_lines.append(line)

    # Parse cues: collect the text portions only (skip timestamp / position lines)
    timestamp_re = re.compile(r"^\d{2}:\d{2}:\d{2}\.\d{3} -->")
    inline_tag_re = re.compile(r"<[^>]+>")

    raw_captions = []
    for line in content_lines:
        stripped = line.strip()
        if not stripped:
            continue
        if timestamp_re.match(stripped):
            continue
        if stripped.isdigit():
            # Cue sequence numbers
            continue
        # Remove inline timing/formatting tags
        cleaned = inline_tag_re.sub("", stripped).strip()
        if cleaned:
            raw_captions.append(cleaned)

    # Deduplicate rolling captions.
    # YouTube auto-captions repeat each fragment exactly three times across
    # consecutive cues: once as a tagged line, twice as a clean carry-over.
    # Stripping tags leaves identical consecutive strings. Keep only the last
    # (i.e., remove a line when the very next line is identical).
    deduped = []
    for i, cap in enumerate(raw_captions):
        if i + 1 < len(raw_captions) and raw_captions[i + 1] == cap:
            continue  # skip — a cleaner copy is coming right after
        deduped.append(cap)

    # Join into paragraphs. Insert a paragraph break when a line ends with
    # sentence-final punctuation followed by a new thought (heuristic).
    # For simplicity, join everything with spaces — the transcript is already
    # one continuous monologue and paragraph breaks would be arbitrary.
    text = " ".join(deduped)

    # Collapse multiple spaces
    text = re.sub(r" {2,}", " ", text)

    return text.strip()


def main():
    if len(sys.argv) < 2:
        print("Usage: python clean_vtt.py <input.vtt> [output.txt]", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    vtt_text = input_path.read_text(encoding="utf-8", errors="replace")
    cleaned = clean_vtt(vtt_text)

    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2])
        output_path.write_text(cleaned + "\n", encoding="utf-8")
        print(f"Written to {output_path}")
    else:
        print(cleaned)


if __name__ == "__main__":
    main()
