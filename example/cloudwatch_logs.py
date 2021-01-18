import boto3

from newport_helpers import cloudwatch_logs_helpers

session = boto3.session.Session()
log_sequence_number = cloudwatch_logs_helpers.logs_get_sequence_number(session, 'josjaffe', 'default')

logs = boto3.client('logs')

for i in range(0, 100):
    response, next_sequence_token = cloudwatch_logs_helpers.logs_put_message(session, 'josjaffe', 'default', 'test')
