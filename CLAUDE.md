# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This is a personal English learning project. Each session studies a single English-language tech YouTube video and produces structured notes on both English expressions and the video's technical content.

## File Structure Per Session

Each study session typically produces:

- `transcript.en.vtt` — Raw VTT subtitle file downloaded from YouTube (word-level timestamps, duplicate lines, formatting noise)
- `transcript_clean.txt` — Plain-text version with all VTT markup stripped, one continuous paragraph per speaker segment
- `video_notes.md` — The primary study artifact, containing two parts:
  1. **Part 1: Common English Expressions** — idiomatic/colloquial phrases extracted from the transcript, each with expression name, meaning, a standalone example sentence, and the verbatim quote from the video
  2. **Part 2: Key Content Summary** — structured summary of the video's technical subject matter

## Workflow

1. A YouTube URL is provided as the source.
2. The VTT transcript is processed into `transcript_clean.txt` (strip timestamps, position tags, duplicate caption lines; join into readable prose).
3. `video_notes.md` is authored by reading through the clean transcript and identifying:
   - Informal/idiomatic English expressions worth learning (aim for 15–20 per video)
   - The core technical concepts explained in the video
4. Notes follow the existing format in `video_notes.md` exactly — heading levels, bold labels (`**Expression**`, `**Meaning**`, `**Example**`, `**In the video**`), horizontal rules between entries, and table formatting for the content summary.

## Notes Format Conventions

- Each expression entry uses `---` separators and a numbered `###` heading.
- The "In the video" quote is italicised and taken verbatim from `transcript_clean.txt`.
- The standalone example sentence must be original (not from the video) and illustrate the expression in a different context.
- The content summary in Part 2 uses `###` headings, bullet lists, and markdown tables — match the density and depth already in the file.
