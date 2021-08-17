import boto3
import json
import jmespath

from newport_helpers import org_helpers
import threading


def process_accounts(account, session, results):
    account_results = []
    s3 = session.client('s3')
    response = s3.list_buckets()
    buckets = jmespath.search("Buckets[].Name", response)
    for bucket in buckets:
        account_results.append(bucket)

    account_total = {'account_id': account, 'buckets': account_results}
    results.append(account_total)
    print(session)
    iam = session.client('iam')

    try:
        cfn = session.client('cloudformation')
        response = cfn.delete_stack(StackName=f"alameda-aardvark-child-{account}")
        print(response)
        print(response)
    except Exception as e:
        print(e)
    return


def main():
    results = []
    threads = []
    for account, session in org_helpers.org_loop_entry():
        process_accounts(account, session, results)

if __name__ == '__main__':
    main()
