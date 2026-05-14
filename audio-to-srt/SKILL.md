---
name: audio-to-srt
description: Transcribe audio or video files to SRT subtitles using faster-whisper. Use when the user asks to transcribe audio to text, generate subtitles from video, create .srt files, convert speech to text with timestamps, or extract spoken content from media files. Supports audio formats (mp3, wav, m4a, flac, aac, ogg, opus) and video formats (mp4, mkv, avi, mov, wmv, flv, webm, m4v). Automatically detects spoken language and generates SRT file in the same directory as input.
---

# Audio To SRT

## Overview

Transcribe audio or video files to SRT subtitle format using `faster-whisper` - a fast, local implementation of OpenAI's Whisper model. The skill automatically detects language, extracts audio from video files if needed, and generates properly formatted SRT files with timestamps.

## Requirements

Install dependencies:

```bash
pip install faster-whisper
```

For video files, [ffmpeg](https://ffmpeg.org/download.html) must be installed and available in PATH.

## Quick Start

Basic usage - transcribe any audio or video file:

```bash
python scripts/transcribe.py path/to/audio.mp3
python scripts/transcribe.py path/to/video.mp4
```

The SRT file is generated in the same directory as the input with the same base name.

## Options

| Parameter | Description | Default | Choices |
|-----------|-------------|---------|---------|
| `--model`, `-m` | Model size (trade-off: speed vs accuracy) | `small` | `tiny`, `base`, `small`, `medium`, `large-v2`, `large-v3` |
| `--language`, `-l` | Language code (auto-detect if omitted) | `auto` | `en`, `zh`, `ja`, `es`, `fr`, etc. |
| `--compute-type` | Computation type | `int8` | `float16`, `int8`, `int8_float16` |

## Model Size Guide

| Model | RAM | Speed | Accuracy |
|-------|-----|-------|----------|
| tiny | ~1GB | Fastest | Basic |
| base | ~1GB | Fast | Good |
| small | ~2GB | Balanced | Very Good |
| medium | ~5GB | Slower | Excellent |
| large-v3 | ~10GB | Slowest | Best |

## Examples

Transcribe with specific language:

```bash
python scripts/transcribe.py video.mp4 --language zh
```

Use higher accuracy model:

```bash
python scripts/transcribe.py podcast.mp3 --model medium
```

## SRT Output Format

```
1
00:00:00,000 --> 00:00:03,500
Hello, welcome to this video.

2
00:00:03,500 --> 00:00:07,000
Today we'll discuss speech recognition.
```
