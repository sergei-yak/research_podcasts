#!/usr/bin/env python3
"""
Example script demonstrating how to use the research podcasts converter.
"""

import os
import tempfile
from src.text_extractor import TextExtractor
from src.demo_converter import DemoAudioConverter

def main():
    """Run example conversion."""
    print("Research Podcasts Converter - Example Usage")
    print("=" * 50)
    
    # Create sample research content
    sample_content = """
# Neural Networks in Computer Vision

## Abstract
This paper reviews recent advances in neural networks for computer vision tasks.
Deep learning has revolutionized image recognition, object detection, and semantic segmentation.

## Introduction
Convolutional Neural Networks (CNNs) have become the dominant approach for computer vision.
These architectures can automatically learn hierarchical features from raw pixel data.

## Methodology
We trained several CNN architectures on the ImageNet dataset and evaluated their performance
on various computer vision benchmarks. Our experiments show consistent improvements over
traditional machine learning approaches.

## Results
The proposed architecture achieved 95% accuracy on image classification tasks,
representing a 10% improvement over previous methods.

## Conclusion
Neural networks continue to advance the state-of-the-art in computer vision.
Future work will focus on improving efficiency and reducing computational requirements.
"""
    
    # Create temporary files
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(sample_content)
        input_file = f.name
    
    output_file = input_file.replace('.md', '.mp3')
    
    try:
        print(f"Input file: {input_file}")
        print(f"Output file: {output_file}")
        print()
        
        # Extract text
        print("1. Extracting text from markdown...")
        extractor = TextExtractor()
        text = extractor.extract(input_file)
        print(f"   Extracted {len(text)} characters")
        
        # Convert to audio
        print("2. Converting to audio (demo mode)...")
        converter = DemoAudioConverter()
        result = converter.text_to_audio(
            text, 
            output_file, 
            title="Neural Networks in Computer Vision"
        )
        
        # Check result
        file_size = os.path.getsize(result) / (1024 * 1024)  # MB
        print(f"   Generated audio file: {result}")
        print(f"   File size: {file_size:.2f} MB")
        
        # Check transcript
        transcript_file = result.replace('.mp3', '_transcript.txt')
        if os.path.exists(transcript_file):
            print(f"   Generated transcript: {transcript_file}")
        
        print("\n✅ Conversion completed successfully!")
        print(f"\nTo play the audio file, you can use:")
        print(f"   mpv {result}")
        print(f"   or any MP3 player")
        
    finally:
        # Clean up
        for file_path in [input_file, output_file]:
            if os.path.exists(file_path):
                os.unlink(file_path)
        
        transcript_file = output_file.replace('.mp3', '_transcript.txt')
        if os.path.exists(transcript_file):
            os.unlink(transcript_file)

if __name__ == '__main__':
    main()