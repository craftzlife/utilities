# S3 Empty Bucket Utility

This script deletes **all versions** and **delete markers** from an AWS S3 bucket, including buckets with versioning enabled.

## Requirements

- Python 3.6+
- AWS credentials configured (via environment, `~/.aws/credentials`, or AWS CLI profiles)
- Install dependencies:

```sh
pip install -r requirements.txt
```

## Usage

**Warning:** This will permanently delete all objects, versions, and delete markers in the specified bucket.

```sh
python empty-bucket.py --bucket <bucket-name> [--profile <aws-profile>]
```

- `--bucket`: Name of the S3 bucket to empty (required)
- `--profile`: AWS CLI profile name (optional)

You will be prompted to confirm before deletion.

## Example

```sh
python empty-bucket.py --bucket my-bucket-name --profile my-aws-profile
```

## Notes

- Make sure you have the necessary permissions to delete objects in the bucket.
- This script is irreversible.