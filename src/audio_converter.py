"""
Text-to-speech conversion utilities.
"""

import os
import tempfile
import wave
from typing import Optional
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

from pydub import AudioSegment
from pydub.effects import normalize


class AudioConverter:
    """Convert text to audio using text-to-speech."""
    
    def __init__(self, language: str = 'en', slow: bool = False, use_local: bool = False):
        """
        Initialize the audio converter.
        
        Args:
            language: Language code for TTS (default: 'en')
            slow: Whether to speak slowly (default: False)
            use_local: Use local TTS instead of Google TTS (default: False)
        """
        self.language = language
        self.slow = slow
        self.use_local = use_local or not GTTS_AVAILABLE
        
        if self.use_local and not PYTTSX3_AVAILABLE:
            raise RuntimeError("Local TTS not available. Install pyttsx3 or use Google TTS.")
    
    def text_to_audio_local(self, text: str, output_path: str, title: Optional[str] = None) -> str:
        """
        Convert text to audio using local TTS (pyttsx3).
        
        Args:
            text: Text to convert to speech
            output_path: Path where audio file will be saved
            title: Optional title for the podcast
            
        Returns:
            Path to the generated audio file
        """
        try:
            # Create a podcast-style intro if title is provided
            full_text = text
            if title:
                intro = f"Welcome to this research podcast. Today we're discussing: {title}. "
                full_text = intro + text
            
            # Initialize pyttsx3
            engine = pyttsx3.init()
            
            # Configure voice settings more safely
            try:
                voices = engine.getProperty('voices')
                if voices and len(voices) > 0:
                    # Try to find an English voice or use the first available
                    english_voice = None
                    for voice in voices:
                        if 'en' in voice.id.lower() or 'english' in voice.name.lower():
                            english_voice = voice
                            break
                    
                    if english_voice:
                        engine.setProperty('voice', english_voice.id)
                    else:
                        engine.setProperty('voice', voices[0].id)
            except:
                # If voice setting fails, continue with default
                pass
            
            try:
                rate = engine.getProperty('rate')
                if rate:
                    new_rate = max(100, rate - 50) if self.slow else rate
                    engine.setProperty('rate', new_rate)
            except:
                # If rate setting fails, continue with default
                pass
            
            # Save to temporary WAV file first
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name
                engine.save_to_file(full_text, temp_path)
                engine.runAndWait()
            
            # Convert WAV to MP3 using pydub
            audio = AudioSegment.from_wav(temp_path)
            
            # Normalize audio levels
            audio = normalize(audio)
            
            # Add a brief pause at the beginning and end
            silence = AudioSegment.silent(duration=1000)  # 1 second
            audio = silence + audio + silence
            
            # Export as MP3
            audio.export(output_path, format="mp3", bitrate="192k")
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            return output_path
            
        except Exception as e:
            # Clean up temporary file if it exists
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.unlink(temp_path)
            raise Exception(f"Failed to convert text to audio using local TTS: {str(e)}")
    
    def text_to_audio_google(self, text: str, output_path: str, title: Optional[str] = None) -> str:
        """
        Convert text to audio using Google TTS.
        
        Args:
            text: Text to convert to speech
            output_path: Path where audio file will be saved
            title: Optional title for the podcast
            
        Returns:
            Path to the generated audio file
        """
        try:
            # Create a podcast-style intro if title is provided
            full_text = text
            if title:
                intro = f"Welcome to this research podcast. Today we're discussing: {title}. "
                full_text = intro + text
            
            # Generate TTS audio
            tts = gTTS(text=full_text, lang=self.language, slow=self.slow)
            
            # Use temporary file for TTS output
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                temp_path = temp_file.name
                tts.save(temp_path)
            
            # Load and process audio
            audio = AudioSegment.from_mp3(temp_path)
            
            # Normalize audio levels
            audio = normalize(audio)
            
            # Add a brief pause at the beginning and end
            silence = AudioSegment.silent(duration=1000)  # 1 second
            audio = silence + audio + silence
            
            # Export as high-quality MP3
            audio.export(output_path, format="mp3", bitrate="192k")
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            return output_path
            
        except Exception as e:
            # Clean up temporary file if it exists
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.unlink(temp_path)
            raise Exception(f"Failed to convert text to audio using Google TTS: {str(e)}")

    def text_to_audio(self, text: str, output_path: str, title: Optional[str] = None) -> str:
        """
        Convert text to audio file.
        
        Args:
            text: Text to convert to speech
            output_path: Path where audio file will be saved
            title: Optional title for the podcast
            
        Returns:
            Path to the generated audio file
            
        Raises:
            Exception: If conversion fails
        """
        if self.use_local:
            return self.text_to_audio_local(text, output_path, title)
        else:
            try:
                return self.text_to_audio_google(text, output_path, title)
            except Exception as e:
                # Fallback to local TTS if Google TTS fails
                if PYTTSX3_AVAILABLE:
                    print(f"Google TTS failed ({str(e)}), falling back to local TTS...")
                    self.use_local = True
                    return self.text_to_audio_local(text, output_path, title)
                else:
                    raise e
    
    def chunk_text(self, text: str, max_chars: int = 4500) -> list[str]:
        """
        Split text into chunks suitable for TTS processing.
        
        Args:
            text: Text to split
            max_chars: Maximum characters per chunk
            
        Returns:
            List of text chunks
        """
        if len(text) <= max_chars:
            return [text]
        
        chunks = []
        words = text.split()
        current_chunk = ""
        
        for word in words:
            # Check if adding this word would exceed the limit
            if len(current_chunk) + len(word) + 1 > max_chars:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = word
                else:
                    # Single word is too long, split it
                    chunks.append(word[:max_chars])
                    current_chunk = word[max_chars:]
            else:
                current_chunk += " " + word if current_chunk else word
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def convert_long_text(self, text: str, output_path: str, title: Optional[str] = None) -> str:
        """
        Convert long text to audio by splitting into chunks and combining.
        
        Args:
            text: Text to convert
            output_path: Path for output audio file
            title: Optional title for the podcast
            
        Returns:
            Path to the generated audio file
        """
        chunks = self.chunk_text(text)
        
        if len(chunks) == 1:
            return self.text_to_audio(text, output_path, title)
        
        # Process chunks separately and combine
        audio_segments = []
        temp_files = []
        
        try:
            for i, chunk in enumerate(chunks):
                with tempfile.NamedTemporaryFile(suffix=f'_chunk_{i}.mp3', delete=False) as temp_file:
                    temp_path = temp_file.name
                    temp_files.append(temp_path)
                    
                    # Add title only to first chunk
                    chunk_title = title if i == 0 else None
                    self.text_to_audio(chunk, temp_path, chunk_title)
                    
                    # Load audio segment
                    segment = AudioSegment.from_mp3(temp_path)
                    audio_segments.append(segment)
            
            # Combine all segments
            combined_audio = audio_segments[0]
            for segment in audio_segments[1:]:
                # Add a brief pause between chunks
                pause = AudioSegment.silent(duration=500)  # 0.5 seconds
                combined_audio += pause + segment
            
            # Export combined audio
            combined_audio.export(output_path, format="mp3", bitrate="192k")
            
            return output_path
            
        finally:
            # Clean up temporary files
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)