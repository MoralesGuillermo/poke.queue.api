import os
from azure.storage.queue import QueueClient, BinaryBase64DecodePolicy, BinaryBase64EncodePolicy
from dotenv import load_dotenv

load_dotenv()

class AQueue:
    # Inject the queue name
    def __init__(self, queue_name: str):
        self.azure_sak = os.getenv('AZURE_SAK')
        if not queue_name:
            # Default queue
            queue_name = os.getenv('AZURE_QUEUE_NAME')
        self.queue_name = queue_name
        self.queue_client = QueueClient.from_connection_string(self.azure_sak, self.queue_name)
        self.queue_client.message_decode_policy = BinaryBase64DecodePolicy()
        self.queue_client.message_encode_policy = BinaryBase64EncodePolicy()

    async def insert_message_on_queue(self, message: str):
        message_bytes = message.encode('utf-8')
        self.queue_client.send_message(
            self.queue_client.message_encode_policy.encode(message_bytes)
        )