import boto3
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

    return


def main():
    results = []
    threads = []
    for account, session in NPH.Org_Helpers.org_loop_entry_thread():
        t = threading.Thread(target=process_accounts, args=(account, session, results))
        threads.append(t)
        t.start()

        #process_accounts(account, session, results)
    for thread in threads:
        thread.join()
    print(results)


if __name__ == '__main__':
    main()
