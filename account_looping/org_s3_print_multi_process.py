import boto3
import jmespath
from multiprocessing import Process
import multiprocessing

from newport_helpers import log_helpers, org_helpers, helpers
import newport_helpers
logger = newport_helpers.NewportHelpers().logger

def process_accounts(account, master_session, results, **kwargs):
    try:
        print(account)
        account_results = []
        session = helpers.get_child_session(account, 'OrganizationAccountAccessRole', master_session)
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





if __name__ == '__main__':

    results = multiprocessing.Manager().list()
    procs = []
    kwargs = {}
    master_session = boto3.session.Session()
    for account in org_helpers.get_org_accounts(master_session):
        proc = Process(target=process_accounts,
                       args=(account, master_session, results),
                       kwargs=kwargs)
        procs.append(proc)

        # proc.start()
    for proc in procs:
        proc.start()
        #process_accounts(account, session, results)
    for proc in procs:
        proc.join()
        # print(account)
    print(f"Results: {results}")
