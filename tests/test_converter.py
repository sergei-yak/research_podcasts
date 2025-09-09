"""
Tests for the research podcasts converter.
"""

import os
import tempfile
import unittest
from pathlib import Path

# Add src to path for imports
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from text_extractor import TextExtractor
from demo_converter import DemoAudioConverter


class TestTextExtractor(unittest.TestCase):
    """Test the text extraction functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.extractor = TextExtractor()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temporary files
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_extract_from_text_file(self):
        """Test extracting text from a plain text file."""
        test_content = "This is a test research article about machine learning."
        test_file = os.path.join(self.temp_dir, "test.txt")
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        extracted = self.extractor.extract(test_file)
        self.assertEqual(extracted, test_content)
    
    def test_extract_from_markdown_file(self):
        """Test extracting text from a markdown file."""
        test_content = "# Research Paper\n\nThis is a **test** markdown file."
        test_file = os.path.join(self.temp_dir, "test.md")
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        extracted = self.extractor.extract(test_file)
        self.assertEqual(extracted, test_content)
    
    def test_file_not_found(self):
        """Test handling of non-existent files."""
        with self.assertRaises(FileNotFoundError):
            self.extractor.extract("nonexistent.txt")
    
    def test_unsupported_format(self):
        """Test handling of unsupported file formats."""
        test_file = os.path.join(self.temp_dir, "test.xyz")
        with open(test_file, 'w') as f:
            f.write("test")
        
        with self.assertRaises(ValueError):
            self.extractor.extract(test_file)


class TestDemoAudioConverter(unittest.TestCase):
    """Test the demo audio converter functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.converter = DemoAudioConverter()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temporary files
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_text_to_audio_basic(self):
        """Test basic text to audio conversion."""
        test_text = "This is a short test article about artificial intelligence."
        output_file = os.path.join(self.temp_dir, "test.mp3")
        
        result = self.converter.text_to_audio(test_text, output_file)
        
        self.assertEqual(result, output_file)
        self.assertTrue(os.path.exists(output_file))
        self.assertGreater(os.path.getsize(output_file), 0)
    
    def test_text_to_audio_with_title(self):
        """Test text to audio conversion with title."""
        test_text = "This is a test article."
        title = "Test Research Paper"
        output_file = os.path.join(self.temp_dir, "test_with_title.mp3")
        
        result = self.converter.text_to_audio(test_text, output_file, title)
        
        self.assertEqual(result, output_file)
        self.assertTrue(os.path.exists(output_file))
        
        # Check if transcript file was created
        transcript_file = output_file.replace('.mp3', '_transcript.txt')
        self.assertTrue(os.path.exists(transcript_file))
        
        with open(transcript_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn(title, content)
            self.assertIn(test_text, content)
    
    def test_chunk_text(self):
        """Test text chunking functionality."""
        short_text = "Short text."
        chunks = self.converter.chunk_text(short_text, max_chars=100)
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0], short_text)
        
        long_text = " ".join(["word"] * 1000)  # Create long text
        chunks = self.converter.chunk_text(long_text, max_chars=50)
        self.assertGreater(len(chunks), 1)
        
        # Verify chunks don't exceed max length (with some tolerance for word boundaries)
        for chunk in chunks:
            self.assertLessEqual(len(chunk), 100)  # Allow some flexibility


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete pipeline."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_end_to_end_conversion(self):
        """Test the complete conversion pipeline."""
        # Create test input file
        test_content = """# AI Research Paper
        
        ## Abstract
        Artificial Intelligence is transforming healthcare through machine learning algorithms.
        
        ## Introduction
        This paper explores the applications of AI in medical diagnosis and treatment.
        
        ## Conclusion
        AI shows promising results in improving patient outcomes.
        """
        
        input_file = os.path.join(self.temp_dir, "research.md")
        output_file = os.path.join(self.temp_dir, "research.mp3")
        
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        # Test extraction
        extractor = TextExtractor()
        extracted_text = extractor.extract(input_file)
        self.assertIn("Artificial Intelligence", extracted_text)
        
        # Test conversion
        converter = DemoAudioConverter()
        result = converter.text_to_audio(extracted_text, output_file, "AI Research")
        
        self.assertEqual(result, output_file)
        self.assertTrue(os.path.exists(output_file))
        self.assertGreater(os.path.getsize(output_file), 1000)  # At least 1KB


if __name__ == '__main__':
    unittest.main()