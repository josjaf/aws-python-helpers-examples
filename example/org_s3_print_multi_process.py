import boto3
import jmespath
from newport_helpers import NPH

from multiprocessing import Process
import multiprocessing
manager = multiprocessing.Manager()


NPH = NPH.NPH()

def process_accounts(account, master_session, results, **kwargs):
    try:
        print(account)
        account_results = []
        session = NPH.Helpers.get_child_session(account, 'OrganizationAccountAccessRole', master_session)
        s3 = session.client('s3')
        response = s3.list_buckets()

        buckets = jmespath.search("Buckets[].Name", response)

        for bucket in buckets:
            account_results.append(bucket)

        account_total = {'account_id': account, 'buckets': account_results}
        # print(account_total)
        results.append(account_total)
    except Exception as e:
        print(e)



    return


def main():
    global results
    results = manager.list()
    procs = []
    kwargs = {}
    master_session = boto3.session.Session()
    for account in NPH.Org_Helpers.get_org_accounts(master_session):
        proc = Process(target=process_accounts,
                    args=(account, master_session, results),
                    kwargs=kwargs)
        procs.append(proc)
        proc.start()

        #process_accounts(account, session, results)
    for proc in procs:
        proc.join()
        # print(account)
    print(f"Results: {results}")


if __name__ == '__main__':
    main()
