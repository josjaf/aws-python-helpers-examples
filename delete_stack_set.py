import boto3
import os
from newport_helpers import helpers, cfn_helpers, org_helpers
from botocore.exceptions import ClientError
import botocore
import uuid

import boto3

import time

Helpers = helpers.Helpers()
Cfn_helpers = cfn_helpers.CfnHelpers()
Org_helpers = org_helpers.Organization_Helpers()

def delete_stack_set(session,stack_set_name, accounts):
    cfn = session.client('cloudformation')
    print()
    try:
        print(f"Deleting Stack Set Instances for {stack_set_name}")
        response = cfn.delete_stack_instances(
            StackSetName=stack_set_name,
            Accounts=accounts,
            Regions=[session.region_name],
            RetainStacks=False,
            OperationId=str(uuid.uuid1())
        )
        print(response)
        inprogress = True
        while inprogress:
            try:
                response = cfn.delete_stack_set(
                    StackSetName=stack_set_name
                )
                inprogress = False
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'OperationInProgressException':
                    print(e.response['Error']['Code'])
                    inprogress = True
                    time.sleep(30)
            except Exception as e:
                raise e
        print(f"Operation Out of Progress")
        response = cfn.delete_stack_set(
            StackSetName=stack_set_name
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'StackSetNotFoundException':
            print(f"Stack Set Not Found: {stack_set_name}")
            response = cfn.delete_stack_set(
                StackSetName=stack_set_name
            )
            print(response)
        else:
            print(e)
    return

def main():
    shared_session = boto3.session.Session(profile_name='aws2')
    shared_session = boto3.session.Session(profile_name='orgmaster')

    org_session = boto3.session.Session(profile_name='orgmaster')
    org_accounts = Org_helpers.get_org_accounts(org_session,remove_org_master=False)
    print(org_accounts)

    cfn = org_session.client('cloudformation')
    stack_set_name = 'devops-boundary'
    response = cfn.list_stack_sets(
        Status='ACTIVE'
    )
    stack_sets = [s['StackSetName'] for s in response['Summaries']]
    print(stack_sets)
    for stack_set_name in stack_sets:
        delete_stack_set(shared_session, stack_set_name, org_accounts)


    return

if __name__ == '__main__':
    main()
