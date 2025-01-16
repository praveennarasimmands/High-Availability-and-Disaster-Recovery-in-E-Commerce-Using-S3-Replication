import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import logging

# Configure logging
logging.basicConfig(filename='logs/replication_logs.txt', level=logging.INFO)

# Load S3 configuration
from config.s3_config import config

def setup_srr():
    try:
        # Initialize S3 client
        s3 = boto3.client('s3', region_name=config['source_region'])

        # Create replication configuration
        replication_configuration = {
            'Role': config['iam_role_arn'],
            'Rules': [
                {
                    'ID': 'ECommerceSRRRule',
                    'Status': 'Enabled',
                    'Prefix': '',
                    'Destination': {
                        'Bucket': f'arn:aws:s3:::{config["source_bucket"]}',
                        'StorageClass': 'STANDARD'
                    },
                    'Filter': {},
                    'DeleteMarkerReplication': {'Status': 'Disabled'},
                    'ReplicationTime': {
                        'Status': 'Enabled',
                        'Time': {
                            'Minutes': 15
                        }
                    },
                    'Priority': 1
                }
            ]
        }

        # Apply replication configuration
        s3.put_bucket_replication(
            Bucket=config['source_bucket'],
            ReplicationConfiguration=replication_configuration
        )

        logging.info(f"SRR setup completed within {config['source_bucket']}")

    except (NoCredentialsError, PartialCredentialsError) as e:
        logging.error(f"Error setting up SRR: {e}")
        print(f"Error setting up SRR: {e}")

if __name__ == '__main__':
    setup_srr()
