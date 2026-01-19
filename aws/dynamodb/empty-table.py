import boto3
import argparse

def delete_all_items(table_name, profile_name=None):
    if profile_name:
        session = boto3.Session(profile_name=profile_name)
        print(f"Using profile: {profile_name}")
    else:
        session = boto3.Session()
        print("Using default AWS profile")

    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(table_name)

    key_schema = table.key_schema
    key_names = [key['AttributeName'] for key in key_schema]
    print(f"Table key schema: {key_names}")

    print(f"Deleting all items in table: {table_name}")

    deleted = 0
    scan_kwargs = {}

    while True:
        response = table.scan(**scan_kwargs)
        items = response.get('Items', [])

        if not items:
            break

        with table.batch_writer() as batch:
            for item in items:
                key = {k: item[k] for k in key_names}
                batch.delete_item(Key=key)
                deleted += 1

        print(f"Deleted {len(items)} items in this batch... (Total: {deleted})")

        if 'LastEvaluatedKey' not in response:
            break
        scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']

    print(f"Finished. Total deleted: {deleted} items.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Delete all items from a DynamoDB table.')
    parser.add_argument('--table', required=True, help='Name of the DynamoDB table')
    parser.add_argument('--profile', help='AWS CLI profile name (optional)')
    args = parser.parse_args()

    confirm = input(f"Are you sure you want to delete ALL items in table '{args.table}'? (yes/no): ")
    if confirm.lower() == 'yes':
        delete_all_items(args.table, args.profile)
    else:
        print("Aborted.")
