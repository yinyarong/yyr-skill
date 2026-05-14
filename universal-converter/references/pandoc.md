# Pandoc Advanced Options

## Table of Contents
- Document Formatting
- PDF Options
- Template Customization
- Syntax Highlighting
- Filters

## Document Formatting

### Markdown to PDF with styling
```bash
pandoc input.md -o output.pdf --pdf-engine=xelatex -V CJKmainfont="SimSun"
```

### Custom margins
```bash
pandoc input.md -o output.pdf -V geometry:margin=1in
```

### Page break control
```bash
pandoc input.md -o output.pdf --toc --toc-depth=2
```

## PDF Options

### Different PDF engines
```bash
# PDFLaTeX (default)
pandoc input.md -o output.pdf --pdf-engine=pdflatex

# XeLaTeX (better for CJK)
pandoc input.md -o output.pdf --pdf-engine=xelatex

# LuaLaTeX
pandoc input.md -o output.pdf --pdf-engine=lualatex

# wkhtmltopdf (HTML to PDF)
pandoc input.md -o output.pdf --pdf-engine=wkhtmltopdf
```

### PDF metadata
```bash
pandoc input.md -o output.pdf \
  --metadata title="My Document" \
  --metadata author="Author Name" \
  --metadata subject="Document Subject"
```

## Template Customization

### Use custom template
```bash
pandoc input.md -o output.pdf --template=custom.tex
```

### CSS for HTML output
```bash
pandoc input.md -o output.html -c style.css
```

## Syntax Highlighting

### Specify highlight style
```bash
pandoc input.md -o output.html --highlight-style=pygments
# Styles: pygments, kate, monochrome, espresso, haddock, tango, zenburn
```

## Filters

### Use Lua filters
```bash
pandoc input.md -o output.pdf --lua-filter=filter.lua
```

### Common filters
```bash
# Diagrams with mermaid
pandoc input.md -o output.html --filter mermaid-filter

# Citations
pandoc input.md -o output.pdf --citeproc

# Word count
pandoc input.md --filter pandoc-wordcount
```

## Batch Processing

### Convert entire directory
```bash
for f in *.md; do
  pandoc "$f" -o "${f%.md}.pdf" --pdf-engine=xelatex -V CJKmainfont="SimSun"
done
```

### Watch and auto-convert (requires inotifywait)
```bash
while inotifywait -e modify *.md; do pandoc input.md -o output.pdf; done
```
