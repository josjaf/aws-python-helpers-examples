import boto3
import jmespath
from newport_helpers import NPH
import threading

NPH = NPH.NPH()

def process_accounts(account, master_session, results):
    account_results = []
    session = NPH.Helpers.get_child_session(account, 'OrganizationAccountAccessRole', master_session)
    s3 = session.client('s3')
    response = s3.list_buckets()
    buckets = jmespath.search("Buckets[].Name", response)
    for bucket in buckets:
        account_results.append(bucket)

    account_total = {'account_id': account, 'buckets': account_results}
    results.append(account_total)
    print(session)

    return


def main():
    results = []
    threads = []
    master_session = boto3.session.Session()
    for account in NPH.Org_Helpers.get_org_accounts(master_session):
        t = threading.Thread(target=process_accounts, args=(account, master_session, results))
        threads.append(t)
        t.start()

        #process_accounts(account, session, results)
    for thread in threads:
        thread.join()
    print(results)


if __name__ == '__main__':
    main()
