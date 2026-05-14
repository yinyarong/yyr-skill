---
name: english_url_learning
description: Study English from a tech YouTube video. Given a YouTube URL, downloads the transcript, cleans it, and generates a bilingual study notes file named YYYY.MM.DD-<Video Title>.md with three parts: (1) 15–20 idiomatic/colloquial English expressions each with English meaning, Chinese translation (中文含义), and an original example sentence; (2) 8–12 common English connectors (e.g. "on top of that", "on the other hand") with function, Chinese translation, and example; (3) a structured content summary of the video's technical subject matter in English with Chinese section summaries and key term translations. Use this skill whenever the user provides a YouTube URL for English learning, says anything like "study this video", "learn English from this", "make notes for this video", or pastes a youtu.be / youtube.com link in a learning context.
---

# English URL Learning

Turn a tech YouTube video into structured English study notes in two steps: get the transcript, then generate the notes.

## Requirements

Install yt-dlp (used to download the caption file without downloading the video):

```
pip install yt-dlp
```

Python 3 is required to run the bundled `clean_vtt.py` script.

## Workflow

### Step 1 — Download the English captions

Run this command in the project directory, replacing `<URL>` with the YouTube URL:

```bash
yt-dlp --write-auto-sub --skip-download --sub-lang en --sub-format vtt -o "transcript" "<URL>"
```

This produces `transcript.en.vtt` (auto-generated captions). If the video has manually authored English captions, prefer those (`--sub-lang en` picks them up automatically when available).

If yt-dlp is not installed, tell the user to run `pip install yt-dlp` and retry.

### Step 2 — Clean the VTT into plain text

```bash
python scripts/clean_vtt.py transcript.en.vtt transcript_clean.txt
```

This strips VTT timestamps, inline timing tags (`<00:00:01.200><c>...</c>`), and the duplicate caption lines that YouTube generates, leaving readable prose in `transcript_clean.txt`.

### Step 3 — Get the video title and topic

Run this to extract metadata without downloading anything:

```bash
yt-dlp --get-title --skip-download "<URL>"
```

Use the title (and your reading of the first few paragraphs of the transcript) to write a one-line topic description for the notes header.

### Step 4 — Generate the notes file

Determine today's date in `YYYY.MM.DD` format (e.g. `2026.05.14`). Use the video title (from Step 3) as the latter half of the filename:

```
<YYYY.MM.DD>-<Video Title>.md
```

Example: `2026.05.14-How to Build Claude Agent Teams Better Than 99% of People.md`

Keep the title as-is — do not slugify, lowercase, or abbreviate it.

Read `transcript_clean.txt` fully, then write the dated notes file with the structure below.

### Step 5 — Delete working files

Once the notes file has been written successfully, delete the two intermediate files:

```bash
rm transcript.en.vtt transcript_clean.txt
```

The dated `YYYY.MM.DD-<Video Title>.md` is the **only file that should remain** after the skill completes. The VTT and plain-text transcript are disposable working files and must not be left in the project directory.

---

## Output Format

```markdown
# Video Notes: <Full Video Title>

> Source: <YouTube URL>
> Topic: <one-line description of what the video is about>

---

## Part 1: Common English Expressions

---

### 1. <Expression Name>
- **Expression**: <the phrase and common variants, e.g. "shoot it off / shooting it off to">
- **Meaning**: <plain English definition — one or two sentences>
- **中文含义**: <Chinese translation of the meaning — one or two sentences in Chinese>
- **Example**: <an original sentence you compose, unrelated to the video's topic>
- **In the video**: *"<verbatim quote from transcript_clean.txt>"*

---

### 2. <Expression Name>
...

---

## Part 2: Common English Connectors

---

### 1. <Connector>
- **Connector**: <the connector and common variants, e.g. "on top of that / on top of this">
- **Function**: <what logical or rhetorical job it does — addition, contrast, concession, result, etc.>
- **中文含义**: <Chinese translation and usage note>
- **Example**: <an original sentence you compose, unrelated to the video's topic>
- **In the video**: *"<verbatim quote from transcript_clean.txt>"*

---

### 2. <Connector>
...

---

## Part 3: Key Content Summary

---

### 1. <Section Title in English>（<中文标题>）

> **概要**：<one or two Chinese sentences summarising what this section covers>

<English content: bullet points, tables, prose — as appropriate for the topic>
Annotate key technical terms on first use: `sub-agents (子代理)`, `orchestrator (调度器)`, etc.

...
```

Separate every entry with `---`. Aim for **15–20 expressions** in Part 1 and **8–12 connectors** in Part 2. Use numbered `###` headings throughout all parts.

In Part 3:
- Every `###` section heading must include a Chinese translation in parentheses: `### 3. Prompting Patterns（提示词写法）`
- Every section must open with a `> **概要**：<2–3 Chinese sentences>` blockquote that summarises the section for quick comprehension
- Then write the English body (bullet lists, tables, numbered sub-steps, prose — whatever fits)
- On first use of a technical term, add its Chinese translation in parentheses inline: `plan approval mode (计划审批模式)`
- Do not pad; cover the concepts the video actually explains

---

## Expression Selection Guide

Good expressions to include:
- Phrasal verbs with non-obvious meaning ("spin up", "burn through", "take another pass at")
- Idiomatic collocations ("from the jump", "under the hood", "the big unlock")
- Tech-community slang ("oneshot", "overkill", "pretty polished")
- Informal transition phrases speakers use live ("hop right back into", "get straight into")

Skip:
- Common formal vocabulary a learner would already know ("implement", "configure", "review")
- Expressions that appear only once and are incidental to the topic

The "In the video" quote should be a short, self-contained sentence from `transcript_clean.txt` that shows the expression naturally. Prefer shorter quotes; trim surrounding filler if needed, but do not alter the expression itself.

The **Example** sentence must be original — a completely different scenario from the video — so the learner sees the expression in a new context.

## Connector Selection Guide

Good connectors to include:
- Additive connectors ("on top of that", "not only that", "what's more")
- Contrast / concession ("on the other hand", "that said", "even so")
- Cause / result ("as a result", "that's why", "because of that")
- Sequence / summary ("to start off", "at the end of the day", "long story short")
- Emphasis / clarification ("the thing is", "to be clear", "if anything")

Skip:
- Single-word connectors every learner already knows ("but", "so", "also", "however")
- Connectors that appear only once and are incidental

Each connector entry uses the same five fields as expressions: **Connector**, **Function**, **中文含义**, **Example**, **In the video**. The **Function** field names the rhetorical role (addition, contrast, result, etc.) in one short phrase.

---

## Handling Edge Cases

- **No English captions available**: Tell the user that no English subtitle file exists for this video and stop. Do NOT attempt to download the audio or video file as a workaround.
- **Non-English auto-captions only**: Try `--sub-lang en-orig` or `--sub-lang en-US`; if still unavailable, tell the user no English subtitles are available and stop. Do NOT download audio or video.
- **Transcript is very short** (< 500 words): Warn the user the notes may be thin; proceed and extract whatever expressions are present.
- **User already has transcript files**: Skip Steps 1–2 and proceed from Step 3, using the existing `transcript_clean.txt` (or clean the VTT if only the raw VTT is present).
- **Output filename**: Always use `YYYY.MM.DD-<Video Title>.md`. Never write a plain `video_notes.md` or omit the title from the filename.
