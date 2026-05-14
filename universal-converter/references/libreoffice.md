# LibreOffice Conversion Options

## Table of Contents
- Basic Conversion
- Headless Mode
- Excel/CSV Operations
- Word to PDF
- Batch Operations
- Filter Options

## Basic Conversion

### Convert to PDF
```bash
soffice --headless --convert-to pdf input.docx
soffice --headless --convert-to pdf input.xlsx
soffice --headless --convert-to pdf input.pptx
```

### Convert to HTML
```bash
soffice --headless --convert-to html input.docx
soffice --headless --convert-to html:HTML_StarOffice_5_0 input.docx
```

### Convert to text
```bash
soffice --headless --convert-to txt:Text input.docx
```

## Excel/CSV Operations

### Excel to CSV
```bash
soffice --headless --convert-to csv input.xlsx
```

### Excel to CSV with specific delimiter
```bash
soffice --headless --convert-to csv:"Text - txt - csv (StarCalc)" -infilter="CSV:44,34,76,1" input.xlsx
# Format: filter-options=field-separator,text-delimiter,encoding,first-row

# Tab-separated
soffice --headless --convert-to csv -infilter="CSV:9,34,76,1" input.xlsx

# Semicolon-separated
soffice --headless --convert-to csv -infilter="CSV:59,34,76,1" input.xlsx
```

### CSV to Excel
```bash
soffice --headless --convert-to xlsx input.csv
```

### Multiple sheets to CSV
```bash
soffice --headless --convert-to csv --outdir output_dir input.xlsx
```

### Excel to ODS
```bash
soffice --headless --convert-to ods input.xlsx
```

## Word Operations

### DOCX to PDF
```bash
soffice --headless --convert-to pdf input.docx
```

### DOCX to DOC (legacy)
```bash
soffice --headless --convert-to doc input.docx
```

### DOCX to ODT
```bash
soffice --headless --convert-to odt input.docx
```

### DOCX to RTF
```bash
soffice --headless --convert-to rtf input.docx
```

### RTF to DOCX
```bash
soffice --headless --convert-to docx input.rtf
```

## PowerPoint Operations

### PPTX to PDF
```bash
soffice --headless --convert-to pdf input.pptx
```

### PPTX to PPT (legacy)
```bash
soffice --headless --convert-to ppt input.pptx
```

### PPTX to ODP
```bash
soffice --headless --convert-to odp input.pptx
```

### PPTX to SWF (Flash)
```bash
soffice --headless --convert-to swf input.pptx
```

## Output Directory

### Specify output directory
```bash
soffice --headless --convert-to pdf --outdir /path/to/output input.docx
```

## Batch Operations

### Convert all DOCX to PDF
```bash
for file in *.docx; do soffice --headless --convert-to pdf "$file"; done
```

### Convert all Excel to CSV
```bash
for file in *.xlsx; do soffice --headless --convert-to csv "$file"; done
```

### Recursive directory conversion
```bash
find . -name "*.docx" -exec soffice --headless --convert-to pdf --outdir converted {} \;
```

## Filter Options

### Writer (Word) filters
```bash
# MS Word 97-2003
soffice --headless --convert-to doc:MS Word 97 input.docx

# MS Word 2007+
soffice --headless --convert-to docx:MS Word 2007 XML input.docx

# Rich Text Format
soffice --headless --convert-to rtf:Rich Text Format input.docx

# Plain text
soffice --headless --convert-to txt:Text input.docx
```

### Calc (Excel) filters
```bash
# MS Excel 97-2003
soffice --headless --convert-to xls:MS Excel 97 input.xlsx

# MS Excel 2007+
soffice --headless --convert-to xlsx:MS Excel 2007 XML input.xlsx

# CSV with comma separator
soffice --headless --convert-to csv:"Text - txt - csv (StarCalc)" -infilter="CSV:44,34,76,1" input.xlsx
```

### Impress (PowerPoint) filters
```bash
# MS PowerPoint 97-2003
soffice --headless --convert-to ppt:MS PowerPoint 97 input.pptx

# MS PowerPoint 2007+
soffice --headless --convert-to pptx:MS PowerPoint 2007 XML input.pptx
```

## Advanced Options

### User profile directory
```bash
soffice --headless -env:UserInstallation=file:///tmp/custom_user_profile --convert-to pdf input.docx
```

### Accept all macros (security risk)
```bash
soffice --headless --infilter="MS Word 2007 XML" --convert-to pdf --accept-all input.docx
```

### Display settings
```bash
soffice --headless --invisible --convert-to pdf input.docx
```

## Troubleshooting

### Check if LibreOffice is running
```bash
pgrep soffice
```

### Kill existing instances
```bash
pkill soffice
```

### Verbose output
```bash
soffice --headless --convert-to pdf --verbose input.docx
```

### Test conversion
```bash
soffice --headless --convert-to pdf --writer input.docx
```

## Python Integration

### Using unoconv (alternative)
```bash
unoconv -f pdf input.docx
unoconv -f csv input.xlsx
unoconv -f html input.docx

# Listener mode (faster batch conversions)
unoconv --listener &
unoconv -f pdf *.docx
```

### Using PyODConverter
```python
from odtfix.docvert import LibreOffice
lo = LibreOffice()
lo.convert('input.docx', 'output.pdf')
```
