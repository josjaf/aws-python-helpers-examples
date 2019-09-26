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
    for bucket in buckets:
        account_results.append(bucket)

    account_total = {'account_id': account, 'buckets': account_results}
    results.append(account_total)
    print(session)
    iam = session.client('iam')

    path = '/'
    role_name = 'josjaffe@amazon.com'
    description = 'A test Role'

    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::805159726499:root"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }

    tags = [
        {
            'Key': 'Environment',
            'Value': 'Production'
        }
    ]

    try:
        response = iam.create_role(
            Path=path,
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description=description,
            MaxSessionDuration=3600,
            Tags=tags
        )
        response = iam.attach_role_policy(
            RoleName=role_name, PolicyArn="arn:aws:iam::aws:policy/AdministratorAccess")

        print(response)
    except Exception as e:
        print(e)
    return


def main():
    results = []
    threads = []
    for account, session in NPH.Org_Helpers.org_loop_entry():
        process_accounts(account, session, results)

if __name__ == '__main__':
    main()
