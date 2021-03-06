from newport_helpers import NPH

NPH = NPH.NPH()


def main():
    env = {'test': 'yes'}
    aws_credentials = NPH.AWSCredentialHelpers.get_credentials()
    combine = {**env, **aws_credentials}
    print(combine)
    run = NPH.Docker_Helpers.run_docker(environment_variables=combine, image_name='hello-world', container_name='newport-helpers-example', command='echo hi')

    return

if __name__ == '__main__':
    main()