from typing import List, Tuple, Set
from dataclasses import dataclass
import pandas as pd
from datetime import datetime
import re

@dataclass
class ValidationError:
    row: int
    column: str
    message: str

class DataValidator:
    REQUIRED_COLUMNS = {'Date', 'Amount'}
    DATE_FORMAT = '%Y-%m-%d'
    AMOUNT_PATTERN = re.compile(r'^[+-]?\d*\.?\d+$')

    @classmethod
    def validate_file(cls, df: pd.DataFrame) -> Tuple[bool, List[ValidationError]]:
        errors = []
        
        header_errors = cls._validate_headers(df.columns)
        errors.extend(header_errors)
        
        if header_errors:
            return False, errors
            
        data_errors = cls._validate_data(df)
        errors.extend(data_errors)
        
        return len(errors) == 0, errors

    @classmethod
    def _validate_headers(cls, columns: List[str]) -> List[ValidationError]:
        errors = []
        columns_set = set(columns)
        
        missing_columns = cls.REQUIRED_COLUMNS - columns_set
        if missing_columns:
            errors.append(
                ValidationError(
                    row=-1,
                    column="N/A",
                    message=f"Missing required columns: {', '.join(missing_columns)}"
                )
            )
        
        duplicate_columns = [col for col in columns if list(columns).count(col) > 1]
        if duplicate_columns:
            errors.append(
                ValidationError(
                    row=-1,
                    column="N/A",
                    message=f"Duplicate columns found: {', '.join(set(duplicate_columns))}"
                )
            )
        
        return errors

    @classmethod
    def _validate_data(cls, df: pd.DataFrame) -> List[ValidationError]:
        errors = []
        
        for idx, date_str in enumerate(df['Date'], start=1):
            try:
                if pd.isna(date_str):
                    raise ValueError("Date cannot be empty")

                datetime.strptime(str(date_str)[:10], cls.DATE_FORMAT)
            except ValueError as e:
                errors.append(
                    ValidationError(
                        row=idx,
                        column='Date',
                        message=f"Invalid date format. Expected YYYY-MM-DD, got: {date_str}"
                    )
                )

        for idx, amount in enumerate(df['Amount'].astype(str), start=1):
            try:
                if pd.isna(amount):
                    raise ValueError("Amount cannot be empty")
                    
                cleaned_amount = amount.strip().lstrip('+')
                
                if not cls.AMOUNT_PATTERN.match(cleaned_amount):
                    raise ValueError("Invalid amount format")
                    
                float(cleaned_amount)
                
            except ValueError as e:
                errors.append(
                    ValidationError(
                        row=idx,
                        column='Amount',
                        message=f"Invalid amount format: {amount}"
                    )
                )
        
        return errors