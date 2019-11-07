import boto3
import jmespath
from newport_helpers import NPH

NPH = NPH.NPH()


def process_accounts(account, session, results):
    iam = session.client('iam')
    user_name = 'Isengard'
    response = iam.create_user(
        UserName=user_name,
        Tags=[
            {
                'Key': 'App',
                'Value': 'Isengard'
            },
        ]
    )
    create_key_response = iam.create_access_key(
        UserName=user_name
    )
    response = iam.attach_user_policy(
        UserName=user_name,
        PolicyArn='arn:aws:iam::aws:policy/AdministratorAccess'
    )
    print()
    print(account)
    print(create_key_response)
    print()
    return


def main():
    results = []
    accounts = """229815083608
479840272640
910499842225
018084485989
698967985654
573919868080
413311410807
448460069026
445577900706"""
    for account in accounts.splitlines():
        child_session = NPH.Helpers.get_child_session(account, 'OrganizationAccountAccessRole', None)

        process_accounts(account, child_session, results)
    # print(results)


if __name__ == '__main__':
    main()
