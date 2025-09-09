"""
Main CLI application for converting research articles to audio podcasts.
"""

import os
import sys
from pathlib import Path
import click
from src.text_extractor import TextExtractor
from src.audio_converter import AudioConverter
from src.demo_converter import DemoAudioConverter


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output audio file path (default: same name as input with .mp3 extension)')
@click.option('--title', '-t', help='Podcast title (default: filename)')
@click.option('--language', '-l', default='en', help='Language code for text-to-speech (default: en)')
@click.option('--slow', is_flag=True, help='Speak slowly')
@click.option('--local', is_flag=True, help='Use local TTS instead of Google TTS')
@click.option('--demo', is_flag=True, help='Demo mode: create placeholder audio with tones')
def convert(input_file, output, title, language, slow, local, demo):
    """
    Convert a research article to an audio podcast.
    
    INPUT_FILE: Path to the research article (PDF, TXT, or MD file)
    """
    try:
        # Determine output path
        if not output:
            input_path = Path(input_file)
            output = input_path.with_suffix('.mp3')
        
        # Determine title
        if not title:
            title = Path(input_file).stem.replace('_', ' ').replace('-', ' ').title()
        
        click.echo(f"Converting '{input_file}' to audio podcast...")
        click.echo(f"Title: {title}")
        click.echo(f"Output: {output}")
        
        # Extract text from input file
        click.echo("Extracting text...")
        extractor = TextExtractor()
        text = extractor.extract(input_file)
        
        if not text.strip():
            click.echo("Error: No text found in the input file.", err=True)
            sys.exit(1)
        
        click.echo(f"Extracted {len(text)} characters")
        
        # Convert text to audio
        if demo:
            click.echo("Converting to audio (DEMO MODE - creates placeholder audio)...")
            converter = DemoAudioConverter(language=language, slow=slow)
        else:
            click.echo("Converting to audio...")
            converter = AudioConverter(language=language, slow=slow, use_local=local)
        
        # Use progress bar for long conversions
        with click.progressbar(length=1, label='Generating audio') as bar:
            output_path = converter.convert_long_text(text, str(output), title)
            bar.update(1)
        
        click.echo(f"✅ Podcast created successfully: {output_path}")
        
        # Show file size
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
        click.echo(f"File size: {file_size:.2f} MB")
        
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@click.group()
def cli():
    """Research Podcasts - Convert research articles to audio podcasts."""
    pass


@cli.command()
def info():
    """Show information about supported file formats and features."""
    click.echo("Research Podcasts Converter")
    click.echo("=" * 30)
    click.echo()
    click.echo("Supported input formats:")
    click.echo("  • PDF files (.pdf)")
    click.echo("  • Text files (.txt)")
    click.echo("  • Markdown files (.md)")
    click.echo()
    click.echo("Features:")
    click.echo("  • Automatic text extraction")
    click.echo("  • Text-to-speech conversion")
    click.echo("  • High-quality MP3 output")
    click.echo("  • Multiple language support")
    click.echo("  • Podcast-style formatting with intro")
    click.echo()
    click.echo("Usage example:")
    click.echo("  python main.py convert research_paper.pdf")
    click.echo("  python main.py convert article.txt --title 'My Research' --language en")


# Add the convert command to the CLI group
cli.add_command(convert)


if __name__ == '__main__':
    cli()