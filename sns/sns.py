#!/usr/bin/env python
# Sample script by Pawel Kilian (en0x)

import argparse
import sys
import boto3
from botocore.exceptions import ClientError

def get_subscription(token=None):
  #  subscriptions = sns.list_subscriptions_by_topic(TopicArn=ARGS_ARN_TOPIC)
    paginator = sns.get_paginator('list_subscriptions_by_topic')
    page_iterator = paginator.paginate(TopicArn=ARGS_ARN_TOPIC)

    for page in page_iterator:
        for key in page[ "Subscriptions" ]:
            if ARGS_EMAIL in key['Endpoint']:
                return 'email ALREADY subscribed! email: {} ; status: {}'.format(key["Endpoint"], key['SubscriptionArn'])
    else:
        sns.subscribe(TopicArn=ARGS_ARN_TOPIC, Protocol="email", Endpoint=ARGS_EMAIL)
        return 'email NOT subscribed! SUBSCRIBING! email: {}; status: {}'.format(key["Endpoint"], key['SubscriptionArn'])


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("--region", help="aws region", default="us-east-1")
    PARSER.add_argument(
        "--email", help="email address of the subscriber", required=True)
    PARSER.add_argument("--arn_topic", help="arn topic", required=True)
    ARGS = PARSER.parse_args()

    if len(sys.argv) == 1 or len(sys.argv) == 3:
        # display help message when no args are passed.
        PARSER.print_help()
        sys.exit(1)

    if ARGS.email:
        ARGS_EMAIL = ARGS.email
    if ARGS.arn_topic:
        ARGS_ARN_TOPIC = ARGS.arn_topic
    if ARGS.region:
        ARGS_REGION = ARGS.region

    sns = boto3.client('sns', region_name=ARGS_REGION)

    try:
        # Get account ids
        ARN_TOPIC_ACCOUNT_ID = ARGS_ARN_TOPIC.split(':')[4]
        ACCOUNT_ID = boto3.client('sts').get_caller_identity().get('Account')
        # If accounts don't match. Print error message and exit, otherwise subscribe to the topic
        if ACCOUNT_ID != ARN_TOPIC_ACCOUNT_ID:
            print "ERROR: Your credential account id: " + ACCOUNT_ID + " is different than arn topic account id: " + ARN_TOPIC_ACCOUNT_ID
            sys.exit(1)
        else:
            SUBSCRIPTION = get_subscription()
            print SUBSCRIPTION

    except ClientError as e:
        if e.response['Error']['Code'] == 'ExpiredToken':
            print "ERROR: Security token expired"
        if e.response['Error']['Code'] == 'InvalidClientTokenId':
            print "ERROR: Security token in invalid"
        else:
            print "Unexpected error: %s" % e




