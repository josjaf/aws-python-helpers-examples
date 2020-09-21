import boto3
import json
import jmespath
from newport_helpers import NPH
import threading

NPH = NPH.NPH()

def process_accounts(account, session, results):
    account_results = []
    s3 = session.client('s3')
    response = s3.list_buckets()
    buckets = jmespath.search("Buckets[].Name", response)
    iam = session.client('iam')

    response = iam.list_users()
    users = jmespath.search("Users[].UserName", response)
    # for user in users:
    #     response = iam.delete_user(
    #         UserName=user
    #     )
    #     print(response)
    results.append({'account': account, 'users': users})

def main():
    results = []
    threads = []
    for account, session in NPH.Org_Helpers.org_loop_entry():
        process_accounts(account, session, results)
    print(results)
if __name__ == '__main__':
    main()
