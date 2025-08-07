import boto3
import argparse

def delete_all_object_versions(bucket_name, profile_name=None):
    if profile_name:
        session = boto3.Session(profile_name=profile_name)
        print(f"Using profile: {profile_name}")
    else:
        session = boto3.Session()
        print("Using default AWS profile")

    s3 = session.client('s3')
    paginator = s3.get_paginator('list_object_versions')

    print(f"Deleting all versions and delete markers in bucket: {bucket_name}")

    deleted = 0
    for page in paginator.paginate(Bucket=bucket_name):
        objects_to_delete = []

        for version in page.get('Versions', []):
            objects_to_delete.append({
                'Key': version['Key'],
                'VersionId': version['VersionId']
            })

        for marker in page.get('DeleteMarkers', []):
            objects_to_delete.append({
                'Key': marker['Key'],
                'VersionId': marker['VersionId']
            })

        if objects_to_delete:
            response = s3.delete_objects(
                Bucket=bucket_name,
                Delete={'Objects': objects_to_delete}
            )
            deleted += len(response.get('Deleted', []))
            print(f"Deleted {len(response.get('Deleted', []))} objects in this batch...")

    print(f"Finished. Total deleted: {deleted} versions and markers.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Delete all versions from an S3 bucket.')
    parser.add_argument('--bucket', required=True, help='Name of the S3 bucket')
    parser.add_argument('--profile', help='AWS CLI profile name (optional)')
    args = parser.parse_args()

    confirm = input(f"Are you sure you want to delete ALL versions in bucket '{args.bucket}'? (yes/no): ")
    if confirm.lower() == 'yes':
        delete_all_object_versions(args.bucket, args.profile)
    else:
        print("Aborted.")
