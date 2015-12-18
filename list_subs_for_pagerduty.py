# Script to create SNS subscriptions from existing SNS topics
#
# python setup_subs_for_pagerduty.py <aws_access_key> <aws_secret_key> <aws_region>
#
# requires bucket in S3 to be created beforehand. Zone files will be zipped up in a file with name
# YYYY-MM-DD_zone_file_extract.zip.
#
# @param    aws_access_key      AWS access key
# @param    aws_secret_key      AWS secret key
# @param    aws_region          AWS region where SNS topics are

import boto3
#import re
import sys

__author__ = 'chhuey'

aws_access_key = sys.argv[1]
aws_secret_key = sys.argv[2]
region_name = sys.argv[3]

sev1_pd_webhook = "https://events.pagerduty.com/adapter/cloudwatch_sns/v1/3b3ddc578ef84d3a801d101e568fcefa"

aws_session = boto3.session.Session(aws_access_key, aws_secret_key, None, region_name)

sns_client = aws_session.client('sns', region_name)

# Auditing section - determines the number of subscriptions there are
subscriptions = sns_client.list_subscriptions()
sub_count = 0
has_more_subs = subscriptions['NextToken']

while has_more_subs is not None:
    sub_count += len(subscriptions['Subscriptions'])
    subscriptions = sns_client.list_subscriptions(NextToken='{0}'.format(has_more_subs))

    subscription_list = subscriptions['Subscriptions']

    for subscription in subscription_list:
        sub_endpoint = subscription['Endpoint']
        print sub_endpoint

        if sub_endpoint == sev1_pd_webhook:
            sub_arn = subscription['SubscriptionArn']
            sns_client.unsubscribe(SubscriptionArn=sub_arn)


    if 'NextToken' in subscriptions:
        has_more_subs = subscriptions['NextToken']
    else:
        has_more_subs = None

print "Subscription count: {0}".format(sub_count)