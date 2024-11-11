from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional
from enum import Enum

import pandas as pd

from services.database import SessionLocal
from models import Account, Transaction
from sqlalchemy.orm import Session

class ProcessingStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    INVALID_FORMAT = "INVALID_FORMAT"

@dataclass
class ProcessingResult:
    successful: bool
    summary: Dict
    status: ProcessingStatus
    error_message: Optional[str] = None

class FileProcessor(ABC):
    @abstractmethod
    def process(self, file_path: str) -> ProcessingResult:
        pass

    def _save_to_db(self, df: pd.DataFrame):
        session: Session = SessionLocal()
        try:
            account = Account(balance=0.0)
            session.add(account)
            session.commit()

            for _, row in df.iterrows():
                transaction = Transaction(
                    account_id=account.id,
                    amount=row['Amount'],
                    transaction_type='credit' if row['Amount'] > 0 else 'debit',
                    transaction_date=row['Date']
                )
                account.balance += row['Amount']
                session.add(transaction)
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()
