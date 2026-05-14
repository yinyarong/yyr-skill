#!/usr/bin/env python3
"""
Audio/Video to SRT Subtitle Generator

This script transcribes audio or video files using faster-whisper
and generates SRT subtitle files in the same directory as the input.

Requirements:
    pip install faster-whisper

Usage:
    python transcribe.py <file_path> [--model_size small]
"""

import argparse
import os
import sys
import subprocess
from datetime import timedelta
from pathlib import Path


def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)."""
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int(td.microseconds / 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def extract_audio(video_path: str, output_path: str) -> str:
    """Extract audio from video file using ffmpeg."""
    try:
        subprocess.run(
            ["ffmpeg", "-i", video_path, "-vn", "-acodec", "pcm_s16le",
             "-ar", "16000", "-ac", "1", "-y", output_path],
            check=True, capture_output=True
        )
        return output_path
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Try with ffmpeg.exe on Windows
        try:
            subprocess.run(
                ["ffmpeg.exe", "-i", video_path, "-vn", "-acodec", "pcm_s16le",
                 "-ar", "16000", "-ac", "1", "-y", output_path],
                check=True, capture_output=True
            )
            return output_path
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError(
                "ffmpeg is required to extract audio from video files. "
                "Install from https://ffmpeg.org/download.html"
            )


def transcribe_to_srt(
    file_path: str,
    model_size: str = "small",
    compute_type: str = "int8",
    language: str = None
) -> str:
    """
    Transcribe audio/video file and generate SRT subtitle file.

    Args:
        file_path: Path to audio or video file
        model_size: faster-whisper model size (tiny, base, small, medium, large-v1, large-v2, large-v3)
        compute_type: Computation type (float16, int8, int8_float16)
        language: Language code (e.g., 'en', 'zh', 'ja'). None for auto-detect.

    Returns:
        Path to generated SRT file
    """
    from faster_whisper import WhisperModel

    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Determine if we need to extract audio
    video_extensions = {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v"}
    audio_extensions = {".mp3", ".wav", ".m4a", ".flac", ".aac", ".ogg", ".wma", ".opus"}

    audio_to_transcribe = None
    temp_audio = None

    if file_path.suffix.lower() in video_extensions:
        # Extract audio from video
        print(f"Extracting audio from video: {file_path.name}")
        temp_audio = file_path.parent / f"{file_path.stem}_temp.wav"
        audio_to_transcribe = extract_audio(str(file_path), str(temp_audio))
    elif file_path.suffix.lower() in audio_extensions:
        audio_to_transcribe = str(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")

    try:
        # Initialize model
        print(f"Loading faster-whisper model: {model_size}...")
        sys.stdout.flush()
        model = WhisperModel(
            model_size,
            device="cpu",
            compute_type=compute_type
        )
        print("Model loaded successfully.")
        sys.stdout.flush()

        # Transcribe - process segments in real-time
        print(f"Starting transcription: {file_path.name}")
        print("(Processing segments as they are detected...)")
        sys.stdout.flush()

        segments, info = model.transcribe(
            audio_to_transcribe,
            language=language,
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500)
        )

        detected_language = info.language
        language_probability = info.language_probability
        print(f"Detected language: {detected_language} (probability: {language_probability:.2f})")
        print("Transcribing (showing every 10 segments):")
        sys.stdout.flush()

        # Generate SRT content - process as segments arrive
        srt_content = []
        segment_count = 0
        duration_info = None

        for segment in segments:
            segment_count += 1

            start_time = format_timestamp(segment.start)
            end_time = format_timestamp(segment.end)
            text = segment.text.strip()

            srt_content.append(f"{segment_count}")
            srt_content.append(f"{start_time} --> {end_time}")
            srt_content.append(text)
            srt_content.append("")  # Empty line between segments

            # Keep track of audio duration
            if duration_info is None:
                duration_info = segment.end

            # Show progress every 10 segments
            if segment_count % 10 == 0:
                print(f"  Segment {segment_count} ({start_time} - {text[:30]}...)", flush=True)

        print(f"Total segments processed: {segment_count}")
        sys.stdout.flush()

        # Write SRT file
        srt_path = file_path.parent / f"{file_path.stem}.srt"
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(srt_content))

        print(f"Subtitle file created: {srt_path}")
        return str(srt_path)

    finally:
        # Clean up temporary audio file
        if temp_audio and temp_audio.exists():
            temp_audio.unlink()


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio/video files to SRT subtitles using faster-whisper"
    )
    parser.add_argument("file", help="Path to audio or video file")
    parser.add_argument(
        "--model", "-m",
        default="small",
        choices=["tiny", "base", "small", "medium", "large-v1", "large-v2", "large-v3"],
        help="Whisper model size (default: small)"
    )
    parser.add_argument(
        "--language", "-l",
        default=None,
        help="Language code (e.g., en, zh, ja). Auto-detect if not specified."
    )
    parser.add_argument(
        "--compute-type",
        default="int8",
        choices=["float16", "int8", "int8_float16"],
        help="Computation type (default: int8)"
    )

    args = parser.parse_args()

    try:
        srt_path = transcribe_to_srt(
            args.file,
            model_size=args.model,
            compute_type=args.compute_type,
            language=args.language
        )
        print(f"\nSuccess! Subtitle saved to: {srt_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
