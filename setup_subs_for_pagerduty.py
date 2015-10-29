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
import re
import sys

__author__ = 'ChienHuey'

aws_access_key = sys.argv[1]
aws_secret_key = sys.argv[2]
region_name = sys.argv[3]

sev1_regex = re.compile(r'sev1$')
sev2_regex = re.compile(r'sev2$')
sns_subscription_protocol = "https"
sev1_pd_webhook = "https://events.pagerduty.com/adapter/cloudwatch_sns/v1/3b3ddc578ef84d3a801d101e568fcefa"
sev2_pd_webhook = "https://events.pagerduty.com/adapter/cloudwatch_sns/v1/6816b651f151448694ad628f9fe5be18"

aws_session = boto3.session.Session(aws_access_key, aws_secret_key, None, region_name)

sns_client = aws_session.client('sns', region_name)

topics = sns_client.list_topics()

sev1_topics = []
sev2_topics = []

# Divide up the topics into two lists, one for SEV1 and one for SEV2
# Creates subscriptions to the PagerDuty webhooks
for topic in topics['Topics']:
    topic_arn = topic['TopicArn']
    match1 = sev1_regex.search(topic_arn)
    match2 = sev2_regex.search(topic_arn)

    if match1 is not None:
        sev1_topics.append(topic_arn)
        sns_client.subscribe(TopicArn='{0}'.format(topic_arn), Protocol='{0}'.format(sns_subscription_protocol),
                             Endpoint='{0}'.format(sev1_pd_webhook))
    elif match2 is not None:
        sev2_topics.append(topic_arn)
        sns_client.subscribe(TopicArn='{0}'.format(topic_arn), Protocol='{0}'.format(sns_subscription_protocol),
                             Endpoint='{0}'.format(sev2_pd_webhook))
    else:
        print "nothing matched"
        print topic_arn

print sev1_topics
print sev2_topics
print sns_client.list_subscriptions()

# Auditing section - determines the number of subscriptions there are
subscriptions = sns_client.list_subscriptions()
sub_count = 0
has_more_subs = subscriptions['NextToken']

while has_more_subs is not None:
    sub_count += len(subscriptions['Subscriptions'])
    subscriptions = sns_client.list_subscriptions(NextToken='{0}'.format(has_more_subs))
    if 'NextToken' in subscriptions:
        has_more_subs = subscriptions['NextToken']
    else:
        has_more_subs = None

print "Subscription count: {0}".format(sub_count)
