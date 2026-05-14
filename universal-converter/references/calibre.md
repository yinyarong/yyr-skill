# Calibre Ebook Conversion Options

## Table of Contents
- Basic Conversion
- Format-Specific Options
- PDF Options
- EPUB Options
- MOBI Options
- Metadata & Cover
- Batch Operations

## Basic Conversion

### EPUB to MOBI (Kindle)
```bash
ebook-convert input.epub output.mobi
```

### EPUB to PDF
```bash
ebook-convert input.epub output.pdf
```

### PDF to EPUB
```bash
ebook-convert input.pdf output.epub
```

### AZW3 to EPUB
```bash
ebook-convert input.azw3 output.epub
```

### TXT to EPUB
```bash
ebook-convert input.txt output.epub
```

## Format-Specific Options

### EPUB Options
```bash
# Disable chapter splitting
ebook-convert input.epub output.mobi --dont-split-on-page-breaks

# Change EPUB version
ebook-convert input.epub output.epub --epub-version=3

# Preserve cover aspect ratio
ebook-convert input.epub output.mobi --preserve-cover-aspect-ratio
```

### MOBI Options
```bash
# MOBI file type
ebook-convert input.epub output.mobi --mobi-file-type=both
# Options: old, new, both

# Inline TOC in MOBI
ebook-convert input.epub output.mobi --inline-toc
```

## PDF Options

### PDF Page Setup
```bash
# Paper size
ebook-convert input.epub output.pdf --pdf-page-size=letter
# Sizes: a0, a1, a2, a3, a4, a5, a6, letter, legal

# Margins (default 72pt)
ebook-convert input.epub output.pdf --pdf-default-font-size=12 --pdf-margin-left=20 --pdf-margin-right=20 --pdf-margin-top=40 --pdf-margin-bottom=40

# Orientation
ebook-convert input.epub output.pdf --pdf-page-orientation=landscape
```

### PDF Fonts
```bash
# Use specific font
ebook-convert input.epub output.pdf --pdf-serif-family="Times New Roman" --pdf-sans-family="Arial"

# Embed fonts
ebook-convert input.epub output.pdf --pdf-embed-font-family="DejaVu Sans"
```

### PDF Layout
```bash
# Number of columns
ebook-convert input.epub output.pdf --pdf-number-of-columns=2

# Page numbers
ebook-convert input.epub output.pdf --pdf-page-numbers --pdf-footer-template="<p>Page _PAGENUM_ of _TOTALPAGES_</p>"

# Custom header/footer
ebook-convert input.epub output.pdf --pdf-header-template="<center>_TITLE_</center>"
```

## Table of Contents

### Auto-generate TOC
```bash
ebook-convert input.epub output.mobi --toc-title="Table of Contents"
```

### TOC threshold
```bash
ebook-convert input.epub output.mobi --toc-threshold=10000  # Words between TOC entries
```

### Level 1/2 TOC
```bash
ebook-convert input.epub output.mobi --toc-levels=2  # Number of levels to include
```

### Disable TOC
```bash
ebook-convert input.epub output.mobi --disable-toc
```

## Metadata & Cover

### Set metadata
```bash
ebook-convert input.epub output.mobi \
  --title "Book Title" \
  --authors "Author Name" \
  --publisher "Publisher" \
  --isbn "1234567890" \
  --tags "fiction,sci-fi" \
  --series "Series Name" \
  --series-index 1
```

### Add cover
```bash
ebook-convert input.epub output.mobi --cover cover.jpg
```

### Extract cover
```bash
ebook-polish --cover cover.jpg input.epub
```

## Text Processing

### Remove hyphens
```bash
ebook-convert input.epub output.mobi --remove-hyphens
```

### Remove paragraph spacing
```bash
ebook-convert input.epub output.mobi --remove-paragraph-spacing
```

### Change indentation
```bash
ebook-convert input.epub output.mobi --indent-paragraphs 2
```

### Line height
```bash
ebook-convert input.epub output.mobi --line-height-factor 1.5
```

## Cleanup Options

### Enable cleanup
```bash
ebook-convert input.epub output.mobi --enable-heuristics --disable-font-rescaling
```

### Specific cleanup
```bash
ebook-convert input.epub output.mobi \
  --unwrap-lines \
  --formatting-type-override=plain \
  --smarten-punctuation
```

## Batch Operations

### Convert all EPUBs in directory
```bash
for file in *.epub; do ebook-convert "$file" "${file%.epub}.mobi"; done
```

### Parallel conversion (GNU parallel)
```bash
ls *.epub | parallel -j4 ebook-convert {} {.}.mobi
```

## Look & Feel

### Change base font size
```bash
ebook-convert input.epub output.mobi --base-font-size=12
```

### Font size mapping
```bash
ebook-convert input.epub output.mobi --font-size-mapping "small=8,normal=12,large=18"
```

### Minimum line height
```bash
ebook-convert input.epub output.mobi --minimum-line-height=12
```

### Extra CSS
```bash
ebook-convert input.epub output.mobi --extra-css "body { text-align: justify; }"
```

## Debugging

### View pipeline
```bash
ebook-convert input.epub output.mobi --debug-pipeline
```

### verbose output
```bash
ebook-convert input.epub output.mobi -vv
```
