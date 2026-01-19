# DynamoDB Empty Table Utility

This script deletes **all items** from an AWS DynamoDB table using efficient batch operations.

## Requirements

- Python 3.6+
- AWS credentials configured (via environment, `~/.aws/credentials`, or AWS CLI profiles)
- Install dependencies:

```sh
pip install -r requirements.txt
```

## Usage

**Warning:** This will permanently delete all items in the specified table.

```sh
python empty-table.py --table <table-name> [--profile <aws-profile>]
```

- `--table`: Name of the DynamoDB table to empty (required)
- `--profile`: AWS CLI profile name (optional)

You will be prompted to confirm before deletion.

## Example

```sh
python empty-table.py --table my-table-name --profile my-aws-profile
```

## Notes

- Make sure you have the necessary permissions to delete items in the table.
- The script automatically detects the table's key schema (partition key and sort key if present).
- Uses batch_writer for efficient deletion of large datasets.
- This script is irreversible.
