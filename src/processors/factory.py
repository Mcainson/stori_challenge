from pathlib import Path
from typing import Optional
from .base import FileProcessor
from .csv_processor import CSVProcessor

class FileProcessorFactory:
    _processors = {
        '.csv': CSVProcessor,
    }

    @classmethod
    def get_processor(cls, file_path: str) -> Optional[FileProcessor]:
        extension = Path(file_path).suffix.lower()
        processor_class = cls._processors.get(extension)
        return processor_class() if processor_class else None
