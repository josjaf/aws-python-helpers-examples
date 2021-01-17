import logging
from botocore.exceptions import ClientError

import boto3
import docker
import datetime
from base64 import b64decode
from newport_helpers import docker_helpers

logger = logging.getLogger(__name__)


def main():
    session = boto3.session.Session()
    ecr_name = 'josjaffe'

    t = datetime.datetime.now()
    buildtime = t.strftime("%m-%d-%Y %H:%M:%S")

    # labels = {'commit': sha, 'buildtime': buildtime}
    # making labels blank to prevent many iterations of the same container with different labaels
    labels = {'buildtime': buildtime}
    path = '.'
    tag = 'ubuntu'
    docker_file = './Dockerfile'
    build_kwargs = dict(tag=tag, docker_file=docker_file, labels=labels, path=path)

    docker_helpers.docker_build_image(**build_kwargs)
    # response, username, password, registry, login_registry = docker_helpers.ecr_login(session, 'josjaffe')
    docker_helpers.ecr_push(session=session, tag=tag, ecr_name=ecr_name)

    return labels


if __name__ == '__main__':
    main()
