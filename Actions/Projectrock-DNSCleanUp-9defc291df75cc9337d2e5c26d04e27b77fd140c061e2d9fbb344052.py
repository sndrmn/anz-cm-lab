import json
import boto3
boto_sts=boto3.client('sts')
def handler(context, inputs):
    print(json.dumps(inputs, indent=2))
    webDNS = str(inputs['customProperties']['customURL'] + ".vmware.education.")
    mongoDNS = str(inputs['customProperties']['customURL'] + "mongodb.vmware.education.")
    
    stsresponse = boto_sts.assume_role(
    RoleArn="arn:aws:iam::435892439035:role/VMWare-UpdateR53Zone-VMware.education",
    RoleSessionName='newsession'
    )
    newsession_id = stsresponse["Credentials"]["AccessKeyId"]
    newsession_key = stsresponse["Credentials"]["SecretAccessKey"]
    newsession_token = stsresponse["Credentials"]["SessionToken"] 

    r53_assumed_client = boto3.client('route53',
        aws_access_key_id=newsession_id,
        aws_secret_access_key=newsession_key,
        aws_session_token=newsession_token
    )
    
    pager = r53_assumed_client.get_paginator('list_resource_record_sets')
    for record_set in pager.paginate(HostedZoneId='Z1GMQQNF9OIM27'):
        for record in record_set['ResourceRecordSets']:
            if record['Name'] == webDNS:
                print(record['ResourceRecords'][0]['Value'])
                print("deleted record")
                r53_assumed_client.change_resource_record_sets(
                    HostedZoneId='Z1GMQQNF9OIM27',
                    ChangeBatch={
                        'Changes': [
                            {
                                'Action': 'DELETE',
                                'ResourceRecordSet': {
                                    'Name': record['Name'],
                                    'Type': record['Type'],
                                    'TTL': record['TTL'],
                                    'ResourceRecords': [{
                                        'Value': record['ResourceRecords'][0]['Value']
                                    }], 
                                }
                            }
                        ]
                    }
                )
    
    pager = r53_assumed_client.get_paginator('list_resource_record_sets')
    for record_set in pager.paginate(HostedZoneId='Z1GMQQNF9OIM27'):
        for record in record_set['ResourceRecordSets']:
            if record['Name'] == mongoDNS:
                print(record['ResourceRecords'][0]['Value'])
                print("deleted record")
                r53_assumed_client.change_resource_record_sets(
                    HostedZoneId='Z1GMQQNF9OIM27',
                    ChangeBatch={
                        'Changes': [
                            {
                                'Action': 'DELETE',
                                'ResourceRecordSet': {
                                    'Name': record['Name'],
                                    'Type': record['Type'],
                                    'TTL': record['TTL'],
                                    'ResourceRecords': [{
                                        'Value': record['ResourceRecords'][0]['Value']
                                    }], 
                                }
                            }
                        ]
                    }
                )