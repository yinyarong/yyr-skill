# ImageMagick Advanced Options

## Table of Contents
- Format Conversion
- Resize & Scale
- Compression & Quality
- Batch Operations
- Special Effects
- Text & Watermarks

## Format Conversion

### HEIC/HEIF to JPG
```bash
magick input.heic output.jpg
# Batch: for file in *.heic; do magick "$file" "${file%.heic}.jpg"; done
```

### WebP to PNG/JPG
```bash
magick input.webp output.jpg
magick input.webp output.png
```

### PNG to JPG (with background)
```bash
magick input.png -background white -flatten output.jpg
```

### AVIF to common formats
```bash
magick input.avif output.jpg
```

### ICO from PNG
```bash
magick input.png -define icon:auto-resize=256,128,64,48,32,16 output.ico
```

### PDF to Images
```bash
# All pages
magick input.pdf output.jpg

# Specific page
magick input.pdf[0] page1.jpg

# Multi-page to single image
magick input.pdf -append output.jpg
```

## Resize & Scale

### Percentage
```bash
magick input.jpg -resize 50% output.jpg
magick input.jpg -resize 150% output.jpg
```

### Exact dimensions (may distort)
```bash
magick input.jpg -resize 800x600! output.jpg
```

### Fit within dimensions (maintain aspect)
```bash
magick input.jpg -resize 800x600 output.jpg
# Or: magick input.jpg -resize x600 output.jpg (height fixed, width auto)
```

### Minimum dimensions (cover)
```bash
magick input.jpg -resize 800x600^ output.jpg
```

### Crop to exact size
```bash
magick input.jpg -resize 800x600^ -gravity center -extent 800x600 output.jpg
```

## Compression & Quality

### JPEG quality (1-100, default 92)
```bash
magick input.jpg -quality 85 output.jpg
```

### PNG compression (level 0-9)
```bash
magick input.png -quality 95 output.png
```

### Progressive JPEG (loads gradually)
```bash
magick input.jpg -interlace Plane output.jpg
```

### Strip metadata (reduce file size)
```bash
magick input.jpg -strip output.jpg
```

### Optimize for web
```bash
magick input.jpg -resize 1200x -quality 80 -strip output.jpg
```

## Batch Operations

### Convert all files in directory
```bash
magick mogrify -format png *.jpg
```

### Resize all images
```bash
magick mogrify -resize 800x600 *.jpg
```

### Add watermark to all
```bash
magick mogrify -draw 'image Over 10 10 0 0 "watermark.png"' *.jpg
```

## Special Effects

### Rotate
```bash
magick input.jpg -rotate 90 output.jpg
magick input.jpg -rotate -45 output.jpg  # counter-clockwise
```

### Flip and flop
```bash
magick input.jpg -flip output.jpg    # vertical
magick input.jpg -flop output.jpg    # horizontal
```

### Grayscale
```bash
magick input.jpg -grayscale Rec709Luminance output.jpg
```

### Blur
```bash
magick input.jpg -blur 0x8 output.jpg  # radiusxsigma
```

### Sharpen
```bash
magick input.jpg -sharpen 0x2 output.jpg
```

### Border
```bash
magick input.jpg -bordercolor white -border 10x10 output.jpg
```

### Rounded corners
```bash
magick input.jpg \( +clone -alpha extract -draw 'circle 50,50 50,0' -alpha on \) -composeDstIn -composite output.png
```

### Shadow
```bash
magick input.png \( +clone -background black -shadow 80x3+5+5 \) +swap -background none -layers merge +repage output.png
```

## Text & Watermarks

### Add text
```bash
magick input.jpg -pointsize 48 -fill white -draw "text 50,50 'Hello World'" output.jpg
```

### Add watermark image
```bash
magick input.jpg watermark.png -gravity southeast -composite output.jpg
```

### Tile watermark
```bash
magick input.jpg \( watermark.png -write mpr:tile +delete -tile mpr:tile \) -compose over -composite output.jpg
```

### Text watermark (diagonal)
```bash
magick input.jpg -rotate 30 -pointsize 50 -fill "rgba(255,255,255,0.3)" -annotate 0 'WATERMARK' -rotate -30 output.jpg
```

## Colors & Filters

### Adjust brightness
```bash
magick input.jpg -brightness-contrast 10x10 output.jpg
```

### Convert to grayscale
```bash
magick input.jpg -type Grayscale output.jpg
```

### Sepia tone
```bash
magick input.jpg -sepia-tone 80% output.jpg
```

### Negate
```bash
magick input.jpg -negate output.jpg
```

### Colorize
```bash
magick input.jpg -fill "#ff0000" -colorize 50% output.jpg
```

## Animation

### Create GIF from images
```bash
magick -delay 100 -loop 0 *.jpg output.gif
```

### Optimize GIF
```bash
magick input.gif -fuzz 10% -layers Optimize output.gif
```

### Resize GIF (preserve animation)
```bash
magick input.gif -coalesce -resize 50% -deconstruct output.gif
```

## PDF Operations

### Images to PDF
```bash
magick *.jpg output.pdf
```

### Multi-page PDF to images
```bash
magick input.pdf output.jpg  # Creates output-0.jpg, output-1.jpg, etc.
```

### Specific PDF page
```bash
magick input.pdf[5] page6.jpg  # Page 6 (0-indexed)
```

## Cropping

### Crop by dimensions
```bash
magick input.jpg -crop 800x600+100+50 output.jpg  # widthxheight+x+y
```

### Crop centered
```bash
magick input.jpg -gravity center -crop 800x600+0+0 output.jpg
```

### Trim borders
```bash
magick input.jpg -trim output.jpg
```

## Information

### Get image info
```bash
magick identify input.jpg
```

### Get detailed info
```bash
magick identify -verbose input.jpg
```

### Get all images in directory
```bash
magick identify *.jpg
```
