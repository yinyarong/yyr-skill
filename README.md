# yyr-skill

![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-blue)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

A personal collection of Claude Code skills for English learning and file operations.

---

## Overview

This repository stores Claude Code skill definitions and their supporting scripts. The three skills cover English study from YouTube videos, audio/video transcription to SRT subtitles, and universal file format conversion. Each skill lives in its own folder and is invoked directly from Claude Code.

---

## Skills

### 1. `english_url_learning` — Study English from a YouTube Video

Given a YouTube URL, downloads the captions, cleans them, and generates a structured bilingual study notes file.

**Output file:** `YYYY.MM.DD-<Video Title>.md`

**Three-part structure:**
- **Part 1 — Common English Expressions** (15–20 entries): idiomatic phrases, phrasal verbs, and tech slang — each with meaning, Chinese translation (中文含义), an original example sentence, and a verbatim quote from the video.
- **Part 2 — Common English Connectors** (8–12 entries): discourse markers like "on top of that" and "on the other hand" — each with function, Chinese translation, example, and in-video quote.
- **Part 3 — Key Content Summary**: structured English summary with Chinese section headings (概要), bilingual term annotations, bullet lists, and tables.

**Workflow:**
1. Download captions with `yt-dlp` (no video download)
2. Strip VTT markup with `scripts/clean_vtt.py`
3. Fetch video title with `yt-dlp --get-title`
4. Write the dated notes file
5. Delete intermediate files (`transcript.en.vtt`, `transcript_clean.txt`)

**Key rules:**
- Never download audio or video files — subtitles only. If no English subtitles exist, stop and report to the user.
- Output filename always follows `YYYY.MM.DD-<Video Title>.md`.

---

### 2. `audio-to-srt` — Transcribe Audio/Video to SRT Subtitles

Transcribes any audio or video file to an SRT subtitle file using `faster-whisper` (local, offline, no API key needed).

**Supported formats:**
- Audio: `mp3`, `wav`, `m4a`, `flac`, `aac`, `ogg`, `opus`
- Video: `mp4`, `mkv`, `avi`, `mov`, `wmv`, `flv`, `webm`, `m4v`

**Usage:**
```bash
python audio-to-srt/scripts/transcribe.py path/to/file.mp4
python audio-to-srt/scripts/transcribe.py path/to/file.mp3 --model medium --language zh
```

**Options:**

| Parameter | Default | Choices |
|---|---|---|
| `--model`, `-m` | `small` | `tiny`, `base`, `small`, `medium`, `large-v2`, `large-v3` |
| `--language`, `-l` | auto-detect | `en`, `zh`, `ja`, `es`, `fr`, … |
| `--compute-type` | `int8` | `float16`, `int8`, `int8_float16` |

**Model size guide:**

| Model | RAM | Speed | Accuracy |
|---|---|---|---|
| tiny | ~1 GB | Fastest | Basic |
| base | ~1 GB | Fast | Good |
| small | ~2 GB | Balanced | Very Good |
| medium | ~5 GB | Slower | Excellent |
| large-v3 | ~10 GB | Slowest | Best |

The SRT file is saved next to the input file with the same base name.

---

### 3. `universal-converter` — Universal File Format Converter

Converts files between formats across six categories using best-in-class CLI tools.

| Category | Tool | Formats |
|---|---|---|
| Documents | Pandoc | Word, PDF, Markdown, HTML, EPUB, LaTeX, PowerPoint |
| Images | ImageMagick | JPG, PNG, WebP, HEIC, GIF, SVG |
| Video | FFmpeg | MP4, MKV, AVI, MOV, WebM |
| Audio | FFmpeg | MP3, AAC, FLAC, OGG, WAV, M4A |
| Ebooks | Calibre | EPUB, MOBI, AZW3, PDF |
| Office/Spreadsheets | LibreOffice | Excel, CSV, PDF, Word, PowerPoint |

See `universal-converter/references/` for detailed options per tool.

---

## Prerequisites

| Requirement | Purpose |
|---|---|
| Python 3.x | `clean_vtt.py`, `transcribe.py` |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Caption download (`english_url_learning`) |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | Transcription (`audio-to-srt`) |
| [ffmpeg](https://ffmpeg.org) | Audio extraction from video (`audio-to-srt`), video/audio conversion (`universal-converter`) |
| [Pandoc](https://pandoc.org) | Document conversion (`universal-converter`) |
| [ImageMagick](https://imagemagick.org) | Image conversion (`universal-converter`) |
| [Calibre](https://calibre-ebook.com) | Ebook conversion (`universal-converter`) |
| [LibreOffice](https://www.libreoffice.org) | Office/spreadsheet conversion (`universal-converter`) |

Not all tools are required — only install what you need for the skills you use.

---

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd 09-yyr-skill

# Install Python dependencies for english_url_learning
pip install yt-dlp

# Install Python dependencies for audio-to-srt
pip install faster-whisper

# Install CLI tools as needed (Windows examples)
winget install yt-dlp.yt-dlp
winget install FFmpeg
winget install JohnMacFarlane.Pandoc
winget install ImageMagick.ImageMagick
winget install Calibre.Calibre
winget install TheDocumentFoundation.LibreOffice
```

---

## Usage

### English URL Learning

Invoke from Claude Code:
```
/english_url_learning https://youtu.be/<video-id>
```

Or say: *"Study English from this video: https://youtu.be/..."*

The skill handles the rest and leaves a single `YYYY.MM.DD-<Video Title>.md` file in the project directory.

### Audio to SRT

```bash
# Basic usage
python audio-to-srt/scripts/transcribe.py recording.mp3

# Video file with Chinese language hint
python audio-to-srt/scripts/transcribe.py lecture.mp4 --language zh

# Higher accuracy model
python audio-to-srt/scripts/transcribe.py podcast.mp3 --model medium
```

### Universal Converter

Invoke from Claude Code by describing the conversion:
```
Convert report.docx to PDF
Convert all JPGs in this folder to WebP
Convert podcast.wav to mp3 at 128k bitrate
```

Or run the underlying tools directly — see `universal-converter/SKILL.md` for the full command reference.

---

## Examples

**1. Study a tech YouTube video:**
```
/english_url_learning https://youtu.be/vDVSGVpB2vc
```
Produces: `2026.05.14-How to Build Claude Agent Teams Better Than 99% of People.md`

**2. Transcribe a Chinese podcast:**
```bash
python audio-to-srt/scripts/transcribe.py episode.mp3 --language zh --model medium
```
Produces: `episode.srt` with timestamped Chinese subtitles.

**3. Batch convert Markdown files to PDF:**
```bash
for file in *.md; do pandoc "$file" -o "${file%.md}.pdf"; done
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `yt-dlp: command not found` | Run `pip install yt-dlp` |
| No English subtitles available | The skill stops and reports — do not use audio download as a workaround |
| `faster-whisper` import error | Run `pip install faster-whisper` |
| `ffmpeg not found` during transcription | Install ffmpeg and ensure it is in PATH |
| Transcription is slow | Use a smaller model (`--model tiny` or `--model base`) |
| Converted document has broken formatting | Try a different target format or adjust Pandoc options (see `references/pandoc.md`) |
| ImageMagick `convert` conflicts with Windows `convert.exe` | Use `magick` instead of `convert` |

---

## Project Structure

```
09-yyr-skill/
├── CLAUDE.md                        # Project instructions for Claude Code
├── english_url_learning/
│   ├── skill.md                     # Skill definition and workflow
│   ├── scripts/
│   │   └── clean_vtt.py             # VTT → plain text cleaner
│   └── evals/
│       ├── evals.json               # Skill evaluation prompts
│       └── files/
│           └── transcript_clean.txt # Eval fixture transcript
├── audio-to-srt/
│   ├── SKILL.md                     # Skill definition
│   └── scripts/
│       └── transcribe.py            # faster-whisper transcription script
└── universal-converter/
    ├── SKILL.md                     # Skill definition and command reference
    └── references/
        ├── pandoc.md
        ├── ffmpeg.md
        ├── imagemagick.md
        ├── calibre.md
        └── libreoffice.md
```

---

## Contributing

1. Fork the repository and create a feature branch.
2. Edit or add skill definitions under their respective folders.
3. Test the skill manually via Claude Code before submitting.
4. Open a pull request with a clear description of what changed and why.

---

## License

No license file is present in this repository. All rights reserved by the author.
