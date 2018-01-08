#!/usr/bin/env python
# Sample script by Pawel Kilian (en0x)

import argparse
import sys
import boto
import boto.sns


def get_subscription(token=None):
    subscriptions = CONN.get_all_subscriptions_by_topic(ARGS_ARN_TOPIC)
    next_token = subscriptions['ListSubscriptionsByTopicResponse'][
        'ListSubscriptionsByTopicResult']['NextToken']
    subscription_list = subscriptions['ListSubscriptionsByTopicResponse'][
        'ListSubscriptionsByTopicResult']['Subscriptions']

    for sub in subscription_list:
        if ARGS_EMAIL in sub['Endpoint']:
            return 'email ALREADY subscribed! email: {} ; status: {}'.format(sub["Endpoint"], sub['SubscriptionArn'])
    else:
        if next_token:
            get_subscription(next_token)
        else:
            CONN.subscribe(ARGS_ARN_TOPIC, "email", ARGS_EMAIL)
            return 'email NOT subscribed! SUBSCRIBING! email: {}; status: {}'.format(sub["Endpoint"], sub['SubscriptionArn'])


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

    # Let's make a connection to sns here
    CONN = boto.sns.connect_to_region(ARGS_REGION)

    # Get account ids
    ARN_TOPIC_ACCOUNT_ID = ARGS_ARN_TOPIC.split(':')[4]
    ACCOUNT_ID = boto.connect_iam().get_user().arn.split(':')[4]

    # If accounts don't match. Print error message and exit, otherwise subscribe to the topic
    if ACCOUNT_ID != ARN_TOPIC_ACCOUNT_ID:
        print "ERROR: Your account id: " + ACCOUNT_ID + " is different than arn topic account id: " + ARN_TOPIC_ACCOUNT_ID
        sys.exit(1)
    else:
        SUBSCRIPTION = get_subscription()
        print SUBSCRIPTION
