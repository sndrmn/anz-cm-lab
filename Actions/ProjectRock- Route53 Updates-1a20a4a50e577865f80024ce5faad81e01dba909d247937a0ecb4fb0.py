import json
import boto3
boto_sts=boto3.client('sts')
def handler(context, inputs):
    #print(json.dumps(inputs, indent=2))
    #Yeah i know its not pretty. could'nt figue out how to return array object without brackets.  This did'nt work input['addesses[0]']' 
    #If you know how to do it gracefully, hook a brother up
    temp = str(inputs['addresses'])
    temp = temp.replace("['", '')
    temp = (temp.replace("']", ''))
    identify_cloud=(temp[len(temp)-4:])
    SendSMS = str(inputs['tags']['SendSMS'])
    
    
    Updated_Number=(inputs['tags']['Number'])
    Updated_Number =(Updated_Number[1:])
    Updated_Number = Updated_Number
    print(Updated_Number)

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
    DNS='projectrock.vmware.education'
    
    #Delete any existing projectrock.vmware.education ResourceRecordSet
    #Done so we can use same DNS record regardless of Cloud Provider used - Azure LB uses IP, AWS LB uses DNS
    
    pager = r53_assumed_client.get_paginator('list_resource_record_sets')
    for record_set in pager.paginate(HostedZoneId='Z1GMQQNF9OIM27'):
        for record in record_set['ResourceRecordSets']:
            if record['Name'] == 'projectrock.vmware.education.':
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
    
    #Insert new DNS record into R53
    #For AWS we create CNAME and Azure we create A record
    if identify_cloud == '.com':
        r53_assumed_client.change_resource_record_sets(
            HostedZoneId='Z1GMQQNF9OIM27',
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': 'projectrock.vmware.education.',
                            'Type': 'CNAME',
                            'TTL': 1,
                            'ResourceRecords': [{
                                'Value': temp
                            }],
                        }
                    }
                ]
            }
        )
    else:
        r53_assumed_client.change_resource_record_sets(
            HostedZoneId='Z1GMQQNF9OIM27',
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': 'projectrock.vmware.education.',
                            'Type': 'A',
                            'TTL': 1,
                            'ResourceRecords': [{
                                'Value': temp
                            }],
                        }
                    }
                ]
            }
        )
    outputs = {
      "Updated_Number": Updated_Number,
      "DNS": DNS,
      "SendSMS": SendSMS 
    }
    return outputs