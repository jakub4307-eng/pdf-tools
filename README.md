# PDF Tools

Two small Python tools for everyday PDF tasks that work **entirely offline**, so sensitive documents never have to be uploaded to online converters.

- **`rotate_pdf.py`** – rotates selected pages of a PDF (90°, -90°, 180°) and saves the result as a new file.
- **`merge_pdf.py`** – merges several PDFs into one, in a chosen order, with an option to normalise all pages to A4.

Both tools have a simple file-picker window for non-technical users and a command-line mode.

## Why I built it

I needed to rotate and merge PDFs containing personal documents and did not want to upload them to third-party websites. I built these tools with the help of an AI assistant (Claude): I described the problem, iterated on the code, and then tested and verified the results myself, including edge cases such as pages of different sizes and orientations.

## Requirements

```
pip install pypdf
```

## Usage

### Simple mode (windows)

Double-click the script or run it without arguments:

```
python rotate_pdf.py
python merge_pdf.py
```

A window will ask you to pick the file(s) and options. The result is saved next to the original file; originals are never modified.

### Command line

```
# Rotate pages 1 and 3 to 5 by 90° clockwise
python rotate_pdf.py input.pdf output.pdf 90 1,3-5

# Merge three files and normalise all pages to A4
python merge_pdf.py merged.pdf a.pdf b.pdf c.pdf --a4
```

## Notes

- Rotation is saved permanently in the file (not just in the viewer).
- A4 normalisation scales and centres each page without cropping; portrait pages stay portrait and landscape pages stay landscape.
- Normalisation changes page size, not image resolution, so low-quality scans will not become sharper.
