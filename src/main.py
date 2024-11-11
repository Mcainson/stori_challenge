from processors.factory import FileProcessorFactory
import os
from services.email_sender import EmailSender

def process_file(file_path: str):
    processor = FileProcessorFactory.get_processor(file_path)
    
    if not processor:
        print(f"No processor available for this file type")
        return
    
    result = processor.process(file_path)

    recipient = os.getenv('RECIPIENT_EMAIL')
    if recipient:
        sender = EmailSender()
        sender.send_summary(recipient, result.summary)
    return result

def main():
    print(f"Processing file...")
    file_path = 'data/transactions.csv'
    result = process_file(file_path)
    if result and result.successful:
        print(f"Processing completed successfully")
        print(f"Total balance: ${result.summary['total_balance']:.2f}")
        print(f"Average credit: ${result.summary['avg_credit']:.2f}")
        print(f"Average debit: ${result.summary['avg_debit']:.2f}")
        
if __name__ == '__main__':
    main()
