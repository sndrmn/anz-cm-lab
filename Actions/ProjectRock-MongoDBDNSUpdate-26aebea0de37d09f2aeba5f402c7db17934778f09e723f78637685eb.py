import json
import boto3
boto_sts=boto3.client('sts')
def handler(context, inputs):
    try:
        temp2 = str(inputs['tags']['server'])
    except:
        print('Tag Does Not Exist')
    else:
        #print(json.dumps(inputs, indent=2))
        temp = str(inputs['addresses'])
        temp = temp.replace("[['", '')
        temp = (temp.replace("']]", ''))

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
    
        r53_assumed_client.change_resource_record_sets(
            HostedZoneId='Z1GMQQNF9OIM27',
            ChangeBatch={
                    'Changes': [
                        {
                            'Action': 'UPSERT',
                            'ResourceRecordSet': {
                                'Name': 'mongodb.vmware.education.',
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