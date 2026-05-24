---
name: english_url_learning
description: Use when user shares video URL + learning intent. Trigger on 学习视频/英语笔记/make notes/study this video/learn English from this/make notes for this video, or pastes a youtu.be/youtube.com/bilibili.com link in a learning context. Also triggers on 学英语/英语学习/看视频学英语.
---

# English URL Learning

Turn a video URL into structured English study notes — expressions, connectors, and bilingual content notes — plus a clean SRT subtitle file.

## What you produce

Save both files to the `downloads/` directory using today's date (`YYYY.MM.DD`) and a short descriptive English slug:

1. **`YYYY.MM.DD_<Title>_Notes.md`** — Three-part study notes
2. **`YYYY.MM.DD_<Title>.srt`** — Clean SRT subtitle file (keep as a deliverable, do NOT delete)

---

## Step 1 — Check for subtitles

```bash
./yt-dlp --list-subs <URL>
```

If `./yt-dlp` doesn't exist, try `yt-dlp` from PATH.

Identify:
- The video's original language
- Whether subtitle tracks exist in that language (manual or auto-generated)

**Stop and prompt the user if** there are no subtitles in the original language, or only AI-translated subtitles exist in other languages:

> "This video has no native-language subtitles. How would you like to proceed?
> 1. Provide an alternative URL (e.g., the YouTube version)
> 2. Use the AI-translated subtitles anyway (quality may be lower)
> 3. Skip this video"

Auto-generated captions in the original language (e.g., YouTube English auto-captions for an English speaker) are acceptable — proceed.

---

## Step 2 — Download the subtitle file

Prefer: manual subtitles in original language → auto-generated in original language.

**YouTube (English video):**
```bash
./yt-dlp --write-auto-subs --sub-lang en --sub-format vtt --skip-download \
  -o "downloads/%(title)s" <URL>
```

**Bilibili or platforms that may require login:**
```bash
./yt-dlp --write-subs --write-auto-subs --sub-lang <lang_code> --skip-download \
  -o "downloads/%(title)s" <URL>
```

If the above returns no subs, retry with `--cookies-from-browser chrome`.

---

## Step 3 — Convert to SRT

**YouTube VTT:** VTT files contain word-level `<c>` timing tags and duplicate cue blocks. Write this script as `convert.py`, run it, then delete both the script and the `.vtt` file. The `.srt` is a final deliverable — keep it.

```python
import re, sys

def vtt_to_srt(vtt_path, srt_path):
    with open(vtt_path, encoding='utf-8') as f:
        content = f.read()
    blocks = re.split(r'\n\n+', content)
    entries = []
    seen = set()
    for block in blocks:
        lines = block.strip().split('\n')
        time_line = next((l for l in lines if '-->' in l), None)
        if not time_line:
            continue
        text_lines = [re.sub(r'<[^>]+>', '', l).strip()
                      for l in lines
                      if '-->' not in l and l.strip()
                      and not l.startswith(('NOTE', 'WEBVTT'))]
        clean = next((t for t in reversed(text_lines) if t), None)
        if not clean or clean in seen:
            continue
        seen.add(clean)
        ts = time_line.split('-->')[0].strip().replace('.', ',')
        te = time_line.split('-->')[1].strip().split()[0].replace('.', ',')
        entries.append([ts, te, clean])
    merged = []
    for e in entries:
        if merged and merged[-1][2] == e[2]:
            merged[-1][1] = e[1]
        else:
            merged.append(e)
    with open(srt_path, 'w', encoding='utf-8') as f:
        for i, (ts, te, text) in enumerate(merged, 1):
            f.write(f"{i}\n{ts} --> {te}\n{text}\n\n")

vtt_to_srt(sys.argv[1], sys.argv[2])
```

Run: `python3 convert.py downloads/input.vtt downloads/YYYY.MM.DD_<Title>.srt`

Then: `rm convert.py downloads/input.vtt`

For non-VTT formats (`.srt`, `.ass`), rename/copy to `downloads/YYYY.MM.DD_<Title>.srt` and skip conversion.

---

## Step 4 — Get the video title

```bash
./yt-dlp --get-title --skip-download "<URL>"
```

Use the title (and the first few paragraphs of the transcript) to write a one-line topic description for the notes header.

---

## Step 5 — Read all subtitle content

SRT files can be large. Read in chunks with `offset` and `limit` (e.g., 400 lines at a time). **Read every chunk before writing any output** — you need the full picture to organize expressions and content coherently.

---

## Step 6 — Write the `_Notes.md` file

The notes file has three parts in order, separated by `---`.

---

### Part 1: English Expressions

Extract **30–40 natural, reusable English expressions**:

- **Phrasal verbs**: *spin up*, *burn through*, *dig into*, *tick up*, *run through*
- **Idioms**: *from the jump*, *under the hood*, *keep me up at night*, *mind-blowing*
- **Tech-community slang**: *oneshot*, *overkill*, *pretty polished*, *the big unlock*
- **Informal transitions**: *hop right back into*, *to be fair*, *to get concrete*
- **Collocations**: *pose a danger to*, *reap the benefits*, *a couple of caveats*

Skip expressions obvious from their component words or too simple to be worth learning.

```markdown
**Video URL:** <URL>

# [English Title] — English Expressions
# [中文标题] — 英语表达学习表

| # | Expression | Original Sentence | Chinese Meaning |
|---|-----------|-------------------|-----------------|
| 1 | **expression** | "sentence with **expression** bolded" | 中文释义 |
```

- Column 2: the expression bolded
- Column 3: verbatim sentence from the video with the expression bolded
- Column 4: Chinese meaning of the expression (not word-for-word translation)
- Order by appearance in the video

---

### Part 2: Common English Connectors

Extract **8–12 connectors** — multi-word phrases that link ideas logically or rhetorically. Write a detailed entry for each:

```markdown
# [English Title] — Common Connectors
# [中文标题] — 英语连接词学习

---

### 1. <Connector>
- **Connector**: <the phrase and common variants, e.g. "on top of that / on top of this">
- **Function**: <rhetorical role in one short phrase — addition, contrast, result, concession, sequence, emphasis>
- **中文含义**: <Chinese translation and usage note>
- **Example**: <an original sentence you compose, in a different context from the video>
- **In the video**: *"<verbatim quote from the SRT>"*
```

Good connectors to target:
- Additive: *on top of that*, *not only that*, *what's more*
- Contrast / concession: *on the other hand*, *that said*, *even so*
- Cause / result: *as a result*, *that's why*, *because of that*
- Sequence / summary: *to start off*, *at the end of the day*, *long story short*
- Emphasis / clarification: *the thing is*, *to be clear*, *if anything*

Skip single-word connectors (*but*, *so*, *also*, *however*) and those that appear only once incidentally.

---

### Part 3: Bilingual Content Notes

Extract and organize the video's knowledge. Focus on reusable, ref-worthy insights — skip filler, repetition, and small talk. **Every English line must be immediately followed by its Chinese translation on the very next line** — headings, body text, list items, table rows, blockquotes, all of it.

```markdown
**Video URL:** <URL>

# [English Title]
# [Chinese Title]

**Source:** [Platform + channel/program name]
**来源：** [中文平台 + 节目名称]

[2–3 sentence bilingual summary of the video's core thesis]

---

## [Topic Section Heading]
## [对应中文标题]

[Organized content: key concepts, data, frameworks, examples, experiments]
```

Suggested sections (adapt to the actual video):
- Core thesis / capability trajectory
- Key risks or frameworks (use a table if there are parallel items)
- Supporting evidence or case studies
- Policy / practical recommendations
- Notable quotes (`>` blockquotes for direct speaker quotes)
- Takeaways / 核心结论 — close with 4–6 bilingual bullet points of the most important actionable insights

---

## File naming

Use today's date (`YYYY.MM.DD`) followed by an underscore and a concise descriptive English slug (not the raw yt-dlp download filename). Examples:
- `2026.03.28_Anthropic_CEO_AI_Risks_Notes.md` + `2026.03.28_Anthropic_CEO_AI_Risks.srt`
- `2026.05.14_Lex_Fridman_Elon_Musk_Notes.md` + `2026.05.14_Lex_Fridman_Elon_Musk.srt`

---

## Edge cases

- **No subtitles in original language**: Prompt the user with the three options in Step 1.
- **Transcript < 500 words**: Warn the user notes may be thin; proceed and extract whatever is present.
- **User already has transcript files**: Skip Steps 1–3 and proceed from Step 4, using the existing SRT.
- **Non-YouTube platform**: Adapt the download command in Step 2 for that platform.
