import pytest
from io import StringIO
from unittest.mock import patch, MagicMock
import pandas as pd
from src.processors.csv_processor import CSVProcessor
from src.processors.base import ProcessingStatus

@pytest.fixture
def sample_csv_file():
    csv_data = """Date,Amount
2023-01-01,100
2023-02-01,-50
"""
    return StringIO(csv_data)

@pytest.fixture
def invalid_csv_file():
    csv_data = """Date,Amount
2023-01-01,100
2023-02-01,invalid_amount
"""
    return StringIO(csv_data)

@pytest.fixture
def empty_csv_file():
    return StringIO("")

@pytest.fixture
def processor():
    return CSVProcessor()

@pytest.fixture
def mock_email_service():
    mock_email = MagicMock()
    mock_email_service = MagicMock(return_value=mock_email)
    return mock_email_service

@patch('src.processors.csv_processor.pd.read_csv')
@patch('src.processors.csv_processor.DataValidator.validate_file')
@patch.object(CSVProcessor, '_save_to_db')
def test_successful_processing(mock_save_to_db, mock_validate_file, mock_read_csv, sample_csv_file, processor):
    mock_df = pd.read_csv(sample_csv_file)
    mock_read_csv.return_value = mock_df
    mock_validate_file.return_value = (True, [])

    result = processor.process('dummy_path.csv')

    assert result.successful
    assert result.status == ProcessingStatus.SUCCESS
    assert 'total_balance' in result.summary
    assert 'transactions_by_month' in result.summary
    assert 'avg_credit' in result.summary
    assert 'avg_debit' in result.summary
    mock_save_to_db.assert_called_once_with(mock_df)

@patch('src.processors.csv_processor.pd.read_csv')
@patch('src.processors.csv_processor.DataValidator.validate_file')
def test_processing_with_errors(mock_validate_file, mock_read_csv, invalid_csv_file, processor):
    mock_df = pd.read_csv(invalid_csv_file)
    mock_read_csv.return_value = mock_df
    mock_validate_file.return_value = (False, [MagicMock(row=1, column='Amount', message='Invalid amount')])

    result = processor.process('dummy_path.csv')

    assert not result.successful
    assert result.status == ProcessingStatus.FAILED
    assert 'Validation failed' in result.error_message

@patch('src.processors.csv_processor.pd.read_csv')
@patch('src.processors.csv_processor.DataValidator.validate_file')
def test_processing_empty_file(mock_validate_file, mock_read_csv, empty_csv_file, processor):
    mock_read_csv.return_value = pd.read_csv(empty_csv_file)
    mock_validate_file.return_value = (True, [])

    result = processor.process('dummy_path.csv')

    assert not result.successful
    assert result.status == ProcessingStatus.FAILED
    assert 'No columns to parse from file' in result.error_message

@patch('src.processors.csv_processor.pd.read_csv')
@patch('src.processors.csv_processor.DataValidator.validate_file')
@patch('src.processors.csv_processor.send_email')
def test_processing_with_exception(mock_send_email, mock_validate_file, mock_read_csv, processor):
    mock_read_csv.side_effect = Exception('File read error')

    result = processor.process('dummy_path.csv')

    assert not result.successful
    assert result.status == ProcessingStatus.FAILED
    assert 'File read error' in result.error_message
    mock_send_email.assert_called_once()