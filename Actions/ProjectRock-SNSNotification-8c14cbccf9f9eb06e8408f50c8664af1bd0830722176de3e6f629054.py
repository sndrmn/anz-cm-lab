import boto3
import time
sns = boto3.client('sns')

def handler(context, inputs):
    Updated_Number=(inputs['Updated_Number'])
    Platform=(inputs['tags']['Platform'])
    AWS_Message = 'Project Rock says: Can you smell what vRA is cooking?  Browse to https://' + inputs['DNS'] + ' to find out.  Please allow 1-2 minutes for DNS propogation'
    Azure_Message = 'Project Rock says: Can you smell what vRA is cooking?  Browse to http://' + inputs['DNS'] + ' to find out.  Please allow 1-2 minutes for DNS propogation'
    vSphere_Message = 'Project Rock says: Can you smell what vRA is cooking?  Browse to http://' + inputs['DNS'] + ' to find out - this was an on-prem deployment so VPN is required.  Please allow 1-2 minutes for DNS propogation'
    
    if Platform == "platform:aws":
        text = AWS_Message
    elif Platform == "platform:azure":
        text = Azure_Message
    else:
        text = vSphere_Message
    
    time.sleep(180)
    
    response = sns.publish(
        PhoneNumber = Updated_Number, 
        Message = text,
        MessageAttributes={
            'AWS.SNS.SMS.SenderID': {
                'DataType': 'String',
                'StringValue': 'PROJECTROCK'
           }
        }
    )
