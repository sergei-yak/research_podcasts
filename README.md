# Research Podcasts

Convert research articles into high-quality audio podcasts using text-to-speech technology.

## Features

- 📄 **Multiple Format Support**: PDF, TXT, and Markdown files
- 🎧 **High-Quality Audio**: Generates 192kbps MP3 podcasts
- 🌍 **Multi-Language**: Supports multiple languages via Google Text-to-Speech
- 🎙️ **Podcast Formatting**: Adds intro and proper pacing
- ⚡ **Smart Processing**: Handles long documents by chunking text appropriately
- 🔄 **Multiple TTS Engines**: Google TTS, local TTS, and demo mode
- 🧪 **Demo Mode**: Create placeholder audio with tones for testing

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

3. (Optional) Install system dependencies for local TTS:
```bash
# For Ubuntu/Debian
sudo apt-get install espeak espeak-data libespeak-dev ffmpeg

# For macOS
brew install espeak ffmpeg
```

## Usage

### Basic Usage

Convert a research paper to audio:
```bash
python main.py convert research_paper.pdf
```

### Demo Mode (No Internet Required)

Create a demo audio file with tones representing speech:
```bash
python main.py convert article.pdf --demo
```

### Advanced Options

```bash
# Specify output file and title
python main.py convert article.pdf --output podcast.mp3 --title "My Research Topic"

# Use different language (requires internet)
python main.py convert paper.txt --language es  # Spanish

# Use local TTS instead of Google TTS
python main.py convert document.md --local

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

## Text-to-Speech Options

### 1. Google Text-to-Speech (Default)
- High-quality natural voices
- Multiple language support
- Requires internet connection
- Automatic fallback to local TTS if unavailable

### 2. Local Text-to-Speech
- Works offline
- Uses system TTS engine (espeak)
- Add `--local` flag to use

### 3. Demo Mode
- Creates placeholder audio with tones
- No TTS dependencies required
- Perfect for testing and development
- Add `--demo` flag to use

## Examples

```bash
# Convert a PDF research paper (default: Google TTS)
python main.py convert "Neural Networks in AI.pdf"

# Convert with custom title and output
python main.py convert research.txt -o my_podcast.mp3 -t "AI Research Overview"

# Convert in Spanish using Google TTS
python main.py convert articulo.pdf --language es

# Use local TTS (offline)
python main.py convert paper.md --local --slow

# Demo mode for testing
python main.py convert document.txt --demo
```

## Output

The converter generates:
- **MP3 audio file**: High-quality podcast audio
- **Transcript file** (demo mode): Text content with metadata

## Requirements

- Python 3.8+
- Internet connection (for Google TTS)
- ffmpeg (automatically handled by pydub)
- espeak (optional, for local TTS)

## How It Works

1. **Text Extraction**: Extracts text from PDFs using advanced parsing
2. **Text Processing**: Chunks long texts for optimal TTS processing
3. **Audio Generation**: Converts text to speech using selected TTS engine
4. **Post-Processing**: Normalizes audio and adds proper podcast formatting
5. **Output**: Saves as high-quality MP3 file

## Development

### Running Tests

```bash
python -m unittest tests.test_converter -v
```

### Example Script

Run the example script to see the converter in action:

```bash
python example.py
```

## Troubleshooting

### Google TTS Issues
- Check internet connection
- Try using `--local` flag for offline conversion
- Use `--demo` flag for testing without TTS

### Local TTS Issues
- Install espeak: `sudo apt-get install espeak espeak-data`
- Try demo mode: `--demo` flag

### Audio Issues
- Ensure ffmpeg is installed
- Check output directory permissions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
