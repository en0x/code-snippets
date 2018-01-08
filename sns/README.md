# SNS

## SNS.py

This script subscribes to SNS topic. It takes 2 required arguments `--email` and `--arn_topic` and subscribes the user to specific topic.
It doesn't resubscribe the email once it's already subscribed or in `pending confirmation` state

### Usage

#### HELP

```
./sns.py -h                                                                                                                                                                                                   (sns-email-subscription|●1✚1)
usage: sns.py [-h] [--region REGION] --email EMAIL --arn_topic ARN_TOPIC

optional arguments:
  -h, --help            show this help message and exit
  --region REGION       aws region
  --email EMAIL         email address of the subscriber
  --arn_topic ARN_TOPIC
                        arn topic
```

- `--email` = required
- `--arn_topic` = required


#### SAMPLE RUN OF EMAIL NOT YET ADDED TO THE TOPIC

```
❯ ./sns.py --email some_email@email.com --arn_topic arn:aws:sns:us-east-1:1234:topic
email NOT subscribed! SUBSCRIBING! email: some_email@email.com; status: PendingConfirmation

```
#### SAMPLE RUN OF ALEADY ADDED EMAIL TO THE TOPIC

```
❯ ./sns.py --email some_email@email.com --arn_topic arn:aws:sns:us-east-1:1234:topic
email ALREADY subscribed! email: some_email@email.com ; status: PendingConfirmation
```

