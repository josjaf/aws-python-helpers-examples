import boto3
import jmespath
from newport_helpers import NPH

NPH = NPH.NPH()



def org_tf(account, session, results):
    account_results = []
    sts = session.client('sts')
    response = sts.get_caller_identity()
    account_id = response['Account']
    structure = """provider "aws" {
  region     = "us-east-1"
  profile = "aws2"
  alias = "aws2"
}"""
    #print(f'\{provider "aws" \nregion     = "us-east-1"\n  profile = "aws2"\n  alias = "aws2"\n')
    line1 = 'provider "aws" {\n'
    line2 = f'\tregion = "{session.region_name}"\n'
    line3 = f'\tprofile = "{account_id}"\n'
    line4 = f'\talias = "{account_id}"\n'
    line5 = "}"

    line = line1 + line2 + line3 + line4 + line5
    print(line)

    return


def main():
    results = []

    for account, session in NPH.Org_Helpers.org_loop_entry():
        org_tf(account, session, results)
    print(results)


if __name__ == '__main__':
    main()
