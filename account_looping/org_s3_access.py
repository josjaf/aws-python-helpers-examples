import boto3
import jmespath
from newport_helpers import org_helpers



def process_accounts(account, session, results):
    account_results = []
    s3control = session.client('s3control')
    sts = session.client('sts')
    account_id = sts.get_caller_identity()['Account']
    response = s3control.put_public_access_block(
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        },
        AccountId=account_id
    )
    print(response)

    return


def main():
    results = []

    for account, session in org_helpers.org_loop_entry():
        process_accounts(account, session, results)
    print(results)


if __name__ == '__main__':
    main()
