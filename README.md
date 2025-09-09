# Research Podcasts

Convert research articles into high-quality audio podcasts using text-to-speech technology.

## Features

- 📄 **Multiple Format Support**: PDF, TXT, and Markdown files
- 🎧 **High-Quality Audio**: Generates 192kbps MP3 podcasts
- 🌍 **Multi-Language**: Supports multiple languages via Google Text-to-Speech
- 🎙️ **Podcast Formatting**: Adds intro and proper pacing
- ⚡ **Smart Processing**: Handles long documents by chunking text appropriately

## Installation

1. Clone this repository:
```bash
git clone https://github.com/sergei-yak/research_podcasts.git
cd research_podcasts
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Convert a research paper to audio:
```bash
python main.py convert research_paper.pdf
```

### Advanced Options

```bash
# Specify output file and title
python main.py convert article.pdf --output podcast.mp3 --title "My Research Topic"

# Use different language
python main.py convert paper.txt --language es  # Spanish

# Slow speech for better comprehension
python main.py convert document.md --slow
```

### Get Help

```bash
python main.py --help
python main.py convert --help
python main.py info  # Show supported formats and features
```

## Supported File Formats

- **PDF** (`.pdf`) - Automatically extracts text from research papers
- **Text** (`.txt`) - Plain text files
- **Markdown** (`.md`) - Markdown documents

## Examples

```bash
# Convert a PDF research paper
python main.py convert "Neural Networks in AI.pdf"

# Convert with custom title and output
python main.py convert research.txt -o my_podcast.mp3 -t "AI Research Overview"

# Convert in Spanish
python main.py convert articulo.pdf --language es
```

## Requirements

- Python 3.8+
- Internet connection (for Google Text-to-Speech)
- ffmpeg (automatically installed with pydub)

## How It Works

1. **Text Extraction**: Extracts text from PDFs using advanced parsing
2. **Text Processing**: Chunks long texts for optimal TTS processing
3. **Audio Generation**: Converts text to speech using Google TTS
4. **Post-Processing**: Normalizes audio and adds proper podcast formatting
5. **Output**: Saves as high-quality MP3 file

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
