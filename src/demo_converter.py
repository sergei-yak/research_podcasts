"""
Simple demo implementation that creates a placeholder audio file with metadata.
"""

import os
import tempfile
from typing import Optional
from pydub import AudioSegment
from pydub.generators import Sine


class DemoAudioConverter:
    """Demo audio converter that creates placeholder audio files."""
    
    def __init__(self, language: str = 'en', slow: bool = False):
        """Initialize the demo converter."""
        self.language = language
        self.slow = slow
    
    def text_to_audio(self, text: str, output_path: str, title: Optional[str] = None) -> str:
        """
        Create a demo audio file with beeps representing the text.
        
        Args:
            text: Text content (used for timing)
            output_path: Output file path
            title: Podcast title
            
        Returns:
            Path to generated audio file
        """
        try:
            # Calculate duration based on text length (roughly 150 words per minute)
            words = len(text.split())
            duration_minutes = max(1, words / 150)  # At least 1 minute
            duration_ms = int(duration_minutes * 60 * 1000)
            
            # Create a simple tone sequence to represent speech
            # Use different frequencies for different sections
            segments = []
            
            # Intro beep if title provided
            if title:
                intro_tone = Sine(800).to_audio_segment(duration=2000)  # 2 seconds
                silence = AudioSegment.silent(duration=1000)  # 1 second pause
                segments.extend([intro_tone, silence])
            
            # Create main content as alternating tones and silence
            remaining_duration = duration_ms - (3000 if title else 0)
            segment_duration = 5000  # 5 second segments
            
            for i in range(0, remaining_duration, segment_duration * 2):
                # Speech tone (lower frequency)
                speech_duration = min(segment_duration, remaining_duration - i)
                if speech_duration > 0:
                    speech_tone = Sine(300).to_audio_segment(duration=speech_duration)
                    segments.append(speech_tone)
                
                # Pause between sentences
                if i + segment_duration < remaining_duration:
                    pause = AudioSegment.silent(duration=500)
                    segments.append(pause)
            
            # Combine all segments
            audio = AudioSegment.empty()
            for segment in segments:
                audio += segment
            
            # Apply basic effects
            audio = audio - 20  # Reduce volume
            
            # Export as MP3
            audio.export(output_path, format="mp3", bitrate="192k")
            
            # Create a text file with the content for reference
            text_file = output_path.replace('.mp3', '_transcript.txt')
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(f"DEMO PODCAST TRANSCRIPT\n")
                f.write(f"========================\n\n")
                if title:
                    f.write(f"Title: {title}\n\n")
                f.write(f"Content:\n{text}\n\n")
                f.write(f"Note: This is a demo implementation. The audio file contains ")
                f.write(f"placeholder tones representing speech patterns.\n")
                f.write(f"Audio Duration: {duration_minutes:.1f} minutes\n")
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Failed to create demo audio: {str(e)}")
    
    def chunk_text(self, text: str, max_chars: int = 4500) -> list[str]:
        """Split text into chunks (same as main implementation)."""
        if len(text) <= max_chars:
            return [text]
        
        chunks = []
        words = text.split()
        current_chunk = ""
        
        for word in words:
            if len(current_chunk) + len(word) + 1 > max_chars:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = word
                else:
                    chunks.append(word[:max_chars])
                    current_chunk = word[max_chars:]
            else:
                current_chunk += " " + word if current_chunk else word
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def convert_long_text(self, text: str, output_path: str, title: Optional[str] = None) -> str:
        """Convert long text (demo version)."""
        return self.text_to_audio(text, output_path, title)