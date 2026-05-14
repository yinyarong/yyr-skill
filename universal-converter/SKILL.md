# Universal File Converter

Universal file format conversion skill supporting documents, images, videos, audio, ebooks, and spreadsheets. Use when users need to convert files between formats: (1) Document conversion (Word/PDF/Markdown/HTML/EPUB/LaTeX/PowerPoint), (2) Image conversion/compression (JPG/PNG/WebP/HEIC/GIF/SVG), (3) Video conversion (MP4/MKV/AVI/MOV/WebM/FLAC), (4) Audio conversion (MP3/AAC/FLAC/OGG/WAV/M4A), (5) Ebook conversion (EPUB/MOBI/AZW3/PDF), (6) Spreadsheet/Office conversion (Excel/CSV/PDF/Word), (7) Batch file conversion.

## Quick Reference

| File Type | Primary Tool | GitHub |
|-----------|--------------|--------|
| Documents | Pandoc | https://github.com/jgm/pandoc |
| Images | ImageMagick | https://github.com/ImageMagick/ImageMagick |
| Video/Audio | FFmpeg | https://github.com/FFmpeg/FFmpeg |
| Ebooks | Calibre | https://github.com/kovidgoyal/calibre |
| Office/Excel | LibreOffice | https://github.com/LibreOffice/core |

## Workflow

1. **Identify source and target formats** - Ask user if unclear
2. **Select appropriate tool** - Based on file type and conversion needed
3. **Check tool availability** - Verify installed or provide install instructions
4. **Execute conversion** - Use proper command syntax
5. **Verify output** - Confirm file was created successfully

## Tool Usage

### Documents (Pandoc)

**Check availability:**
```bash
pandoc --version
```

**Common conversions:**
```bash
# Markdown to PDF
pandoc input.md -o output.pdf

# Markdown to Word
pandoc input.md -o output.docx

# Word to PDF
pandoc input.docx -o output.pdf

# Word to Markdown
pandoc input.docx -o output.md

# HTML to PDF
pandoc input.html -o output.pdf

# EPUB to PDF
pandoc input.epub -o output.pdf
```

**Batch conversion (Bash):**
```bash
for file in *.md; do pandoc "$file" -o "${file%.md}.pdf"; done
```

**Install:**
- Windows: `winget install --id JohnMacFarlane.Pandoc`
- macOS: `brew install pandoc`
- Linux: `sudo apt install pandoc`

### Images (ImageMagick)

**Check availability:**
```bash
magick --version  # or: convert --version
```

**Common conversions:**
```bash
# Convert format
magick input.jpg output.png
convert input.jpg output.png  # older syntax

# Batch convert JPG to PNG
for file in *.jpg; do convert "$file" "${file%.jpg}.png"; done

# Resize and convert
magick input.jpg -resize 800x600 output.jpg

# Compress image
magick input.jpg -quality 80 output.jpg

# Create PDF from images
magick *.jpg output.pdf

# WebP to JPG
magick input.webp output.jpg

# HEIC to JPG (modern)
magick input.heic output.jpg
```

**Install:**
- Windows: `winget install ImageMagick.ImageMagick`
- macOS: `brew install imagemagick`
- Linux: `sudo apt install imagemagick`

### Video (FFmpeg)

**Check availability:**
```bash
ffmpeg -version
```

**Common conversions:**
```bash
# Convert video format
ffmpeg -i input.mp4 output.avi

# MP4 to WebM
ffmpeg -i input.mp4 output.webm

# Compress video
ffmpeg -i input.mp4 -vcodec libx264 -crf 28 output.mp4

# Extract audio from video
ffmpeg -i input.mp4 -vn output.mp3

# Video to GIF
ffmpeg -i input.mp4 output.gif

# Resize video
ffmpeg -i input.mp4 -vf scale=1280:720 output.mp4
```

**Install:**
- Windows: `winget install FFmpeg`
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

### Audio (FFmpeg)

**Common conversions:**
```bash
# Convert audio format
ffmpeg -i input.mp3 output.wav

# MP3 to FLAC
ffmpeg -i input.mp3 -c:a flac output.flac

# Compress audio (lower bitrate)
ffmpeg -i input.wav -b:a 128k output.mp3

# M4A to MP3
ffmpeg -i input.m4a -codec:v copy -codec:a libmp3lame -q:a 2 output.mp3
```

### Ebooks (Calibre)

**Check availability:**
```bash
ebook-convert --version
```

**Common conversions:**
```bash
# EPUB to MOBI
ebook-convert input.epub output.mobi

# EPUB to PDF
ebook-convert input.epub output.pdf

# PDF to EPUB
ebook-convert input.pdf output.epub

# AZW3 to EPUB
ebook-convert input.azw3 output.epub
```

**Install:**
- Windows: `winget install Calibre.Calibre`
- macOS: `brew install --cask calibre`
- Linux: Download from https://calibre-ebook.com/download_linux

### Office/Excel (LibreOffice)

**Check availability:**
```bash
soffice --version  # or: libreoffice --version
```

**Common conversions:**
```bash
# Excel to PDF (Windows)
soffice --headless --convert-to pdf input.xlsx

# Word to PDF
soffice --headless --convert-to pdf input.docx

# Excel to CSV
soffice --headless --convert-to csv input.xlsx

# PPT to PDF
soffice --headless --convert-to pdf input.pptx

# Batch convert Excel to CSV
for file in *.xlsx; do soffice --headless --convert-to csv "$file"; done
```

**Install:**
- Windows: `winget install TheDocumentFoundation.LibreOffice`
- macOS: `brew install --cask libreoffice`
- Linux: `sudo apt install libreoffice`

## Advanced Options

See reference files for detailed options:
- [Pandoc options](references/pandoc.md) - Document formatting, templates
- [FFmpeg options](references/ffmpeg.md) - Codec settings, bitrate control
- [ImageMagick options](references/imagemagick.md) - Advanced image processing
- [Calibre options](references/calibre.md) - Ebook formatting options

## Troubleshooting

**Tool not found:** Provide install instructions for user's OS
**Permission denied:** Check file/directory permissions
**Conversion failed:** Verify input file is not corrupted
**Output quality poor:** Adjust compression/bitrate parameters
**Batch conversion:** Use shell loops or scripting

## Integration Notes

- **Python projects:** Use `pypandoc`, `Pillow`, `ffmpeg-python`, `pyexcel`
- **Node projects:** Use `pandoc-filter`, `sharp`, `fluent-ffmpeg`
- **Docker:** Use [ConvertX](https://github.com/C4illin/ConvertX) for self-hosted web conversion
- **Windows:** Use [FileConverter](https://github.com/Tichau/FileConverter) for right-click integration
