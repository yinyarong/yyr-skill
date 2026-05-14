# FFmpeg Advanced Options

## Table of Contents
- Video Codec Settings
- Audio Codec Settings
- Quality Control
- Format Presets
- Batch Processing

## Video Codec Settings

### H.264 (most compatible)
```bash
ffmpeg -i input.mp4 -c:v libx264 -preset medium -crf 23 output.mp4
```

### H.265/HEVC (better compression)
```bash
ffmpeg -i input.mp4 -c:v libx265 -preset medium -crf 28 output.mp4
```

### VP9 (WebM)
```bash
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 output.webm
```

### AV1 (next-gen)
```bash
ffmpeg -i input.mp4 -c:v libaom-av1 -crf 30 -strict experimental output.mkv
```

## Audio Codec Settings

### AAC (standard)
```bash
ffmpeg -i input.mp4 -c:a aac -b:a 192k output.mp4
```

### MP3 (legacy)
```bash
ffmpeg -i input.mp4 -c:a libmp3lame -b:a 192k output.mp3
```

### Opus (best quality/size)
```bash
ffmpeg -i input.mp4 -c:a libopus -b:a 128k output.opus
```

### FLAC (lossless)
```bash
ffmpeg -i input.wav -c:a flac output.flac
```

## Quality Control

### CRF values (lower = better quality, larger file)
```bash
# 18-28: Visually lossless to good quality (recommended)
# 23: Default for H.264
ffmpeg -i input.mp4 -c:v libx264 -crf 23 output.mp4
```

### Two-pass encoding (consistent quality)
```bash
ffmpeg -i input.mp4 -c:v libx264 -b:v 5M -pass 1 -f mp4 NUL
ffmpeg -i input.mp4 -c:v libx264 -b:v 5M -pass 2 output.mp4
```

### Bitrate targeting
```bash
ffmpeg -i input.mp4 -b:v 2M -maxrate 2.5M -bufsize 5M output.mp4
```

## Format Presets

### Preset speed options
```bash
# ultrafast, superfast, veryfast, faster, fast, medium (default), slow, slower, veryslow
ffmpeg -i input.mp4 -c:v libx264 -preset fast -crf 23 output.mp4
```

### Common device presets
```bash
# YouTube recommended
ffmpeg -i input.mp4 -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 128k output.mp4

# Instagram
ffmpeg -i input.mp4 -vf scale=1080:1080 -c:v libx264 -preset medium -crf 23 output.mp4

# TikTok
ffmpeg -i input.mp4 -vf scale=1080x1920 -c:v libx264 -preset medium -crf 23 output.mp4
```

## Video Manipulation

### Trim video
```bash
# From 00:01:00 to 00:02:00
ffmpeg -i input.mp4 -ss 00:01:00 -to 00:02:00 -c copy output.mp4
```

### Resize video
```bash
# Scale to 720p
ffmpeg -i input.mp4 -vf scale=-1:720 output.mp4

# Scale to specific width, maintain aspect ratio
ffmpeg -i input.mp4 -vf scale=1280:-1 output.mp4

# Fit within 1920x1080, maintain aspect ratio
ffmpeg -i input.mp4 -vf scale="iw*min(1920/iw\,1080/ih):ih*min(1920/iw\,1080/ih)" output.mp4
```

### Change frame rate
```bash
ffmpeg -i input.mp4 -r 30 output.mp4
```

### Extract frames as images
```bash
# One frame per second
ffmpeg -i input.mp4 -vf fps=1 frame_%04d.png

# Every 100 frames
ffmpeg -i input.mp4 -vf "select='not(mod(n,100))'" -vsync 0 frame_%04d.png
```

### Create GIF from video
```bash
# High quality GIF
ffmpeg -i input.mp4 -vf "fps=10,scale=480:-1" -c:v gif output.gif

# With palette (better quality)
ffmpeg -i input.mp4 -vf "fps=10,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" output.gif
```

## Audio Manipulation

### Extract audio from video
```bash
ffmpeg -i input.mp4 -vn -c:a copy output.aac
```

### Remove audio from video
```bash
ffmpeg -i input.mp4 -c:v copy -an output.mp4
```

### Normalize audio volume
```bash
ffmpeg -i input.mp4 -af "loudnorm" output.mp4
```

### Convert sample rate
```bash
ffmpeg -i input.wav -ar 44100 output.wav
```

## Batch Processing

### Convert all MP4 to MP3
```bash
for file in *.mp4; do ffmpeg -i "$file" -vn -c:a libmp3lame -q:a 2 "${file%.mp4}.mp3"; done
```

### Resize all videos in directory
```bash
for file in *.mp4; do ffmpeg -i "$file" -vf scale=1280:-1 "resized_$file"; done
```

## Speed Control

### Speed up/slow down video
```bash
# 2x speed
ffmpeg -i input.mp4 -filter:v "setpts=0.5*PTS" output.mp4

# 0.5x speed (slow motion)
ffmpeg -i input.mp4 -filter:v "setpts=2.0*PTS" output.mp4

# Speed up both video and audio
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" output.mp4
```

## Concatenate Files

### Join videos (same format)
```bash
# Create filelist.txt containing:
# file 'input1.mp4'
# file 'input2.mp4'

ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp4
```
