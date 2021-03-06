import boto3
import json
import jmespath
from newport_helpers import org_helpers
import threading

def process_accounts(account, session, results, local_account_id):

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
                    "AWS": f"arn:aws:iam::{local_account_id}:root"
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
    session = boto3.session.Session()
    local_acount_id = session.client('sts').get_caller_identity()['Account']
    print(local_acount_id)
    results = []
    threads = []
    for account, session in org_helpers.org_loop_entry():
        process_accounts(account, session, results, local_acount_id)

if __name__ == '__main__':
    main()
