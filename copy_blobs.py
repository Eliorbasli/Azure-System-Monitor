import os
from azure.storage.blob import BlobServiceClient
import sys

def copy_blobs():
    # Get the connection strings from environment variables
    storage_account_a_connection_string = os.getenv("STORAGE_ACCOUNT_A_CONNECTION_STRING")
    storage_account_b_connection_string = os.getenv("STORAGE_ACCOUNT_B_CONNECTION_STRING")
    
    # Validate connection strings
    if not storage_account_a_connection_string:
        print("Error: STORAGE_ACCOUNT_A_CONNECTION_STRING environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    
    if not storage_account_b_connection_string:
        print("Error: STORAGE_ACCOUNT_B_CONNECTION_STRING environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Initialize the BlobServiceClient for both storage accounts
        blob_service_client_a = BlobServiceClient.from_connection_string(storage_account_a_connection_string)
        blob_service_client_b = BlobServiceClient.from_connection_string(storage_account_b_connection_string)

        # Access the containers in both storage accounts
        container_a = blob_service_client_a.get_container_client("containerA")
        container_b = blob_service_client_b.get_container_client("containerB")

        # Copy blobs from container A to container B
        for blob in container_a.list_blobs():
            blob_client_a = container_a.get_blob_client(blob.name)
            blob_client_b = container_b.get_blob_client(blob.name)

            # Start copying each blob
            blob_client_b.start_copy_from_url(blob_client_a.url)

        print("Blobs copied successfully!")
    except Exception as e:
        print(f"Error during blob copy operation: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    copy_blobs()
