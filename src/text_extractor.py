"""
Text extraction utilities for research articles.
"""

import os
from typing import Optional
import PyPDF2
import pdfplumber


class TextExtractor:
    """Extract text from various document formats."""
    
    def extract_from_pdf(self, file_path: str) -> str:
        """
        Extract text from PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text as string
            
        Raises:
            FileNotFoundError: If file doesn't exist
            Exception: If extraction fails
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            # Try pdfplumber first (better text extraction)
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                
                if text.strip():
                    return text.strip()
            
            # Fallback to PyPDF2
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                return text.strip()
        
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def extract_from_text(self, file_path: str) -> str:
        """
        Extract text from plain text file.
        
        Args:
            file_path: Path to the text file
            
        Returns:
            File content as string
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception as e:
            raise Exception(f"Failed to read text file: {str(e)}")
    
    def extract(self, file_path: str) -> str:
        """
        Auto-detect file type and extract text.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Extracted text as string
        """
        _, ext = os.path.splitext(file_path.lower())
        
        if ext == '.pdf':
            return self.extract_from_pdf(file_path)
        elif ext in ['.txt', '.md']:
            return self.extract_from_text(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")