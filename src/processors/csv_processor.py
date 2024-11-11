import pandas as pd
from typing import Dict
from .base import FileProcessor, ProcessingResult, ProcessingStatus
from .validators import DataValidator

def _calculate_summary(df: pd.DataFrame) -> Dict:
    return {
        'total_balance': df['Amount'].sum(),
        'transactions_by_month': df.groupby(df['Date'].dt.strftime('%B')).size().to_dict(),
        'avg_credit': df[df['Amount'] > 0]['Amount'].mean(),
        'avg_debit': df[df['Amount'] < 0]['Amount'].mean()
    }


class CSVProcessor(FileProcessor):
    def process(self, file_path: str) -> ProcessingResult:
        try:
            df = pd.read_csv(file_path)
            
            is_valid, validation_errors = DataValidator.validate_file(df)
            
            if not is_valid:
                error_messages = "\n".join([
                    f"Row {err.row}: {err.column} - {err.message}"
                    for err in validation_errors
                ])
                
                print(f"Validation failed:\n{error_messages}")
                return ProcessingResult(
                    successful=False,
                    summary={},
                    status=ProcessingStatus.FAILED,
                    error_message=f"Validation failed:\n{error_messages}"
                )

            df['Date'] = pd.to_datetime(df['Date'])
            summary = _calculate_summary(df)

            self._save_to_db(df)
            
            return ProcessingResult(
                successful=True,
                summary=summary,
                status=ProcessingStatus.SUCCESS
            )
            
        except Exception as e:
            return ProcessingResult(
                successful=False,
                summary={},
                status=ProcessingStatus.FAILED,
                error_message=str(e)
            )
