import boto3
client = boto3.client('ssm')
def handler(context, inputs):
    WebSite = str(inputs['customProperties']['customURL'])
    WebSite = WebSite + '.vmware.education'
    MongoDB = str(inputs['customProperties']['customURL'])
    MongoDB = MongoDB + 'mongodb.vmware.education'
    
    response = client.put_parameter(
    Name='ProjectRockSite',
    Description='ProjectRock Variable referenced in Ansible Playbook',
    Value=WebSite,
    Type='String',
    Overwrite=True,
    Tier='Standard'
    )
    
    response2 = client.put_parameter(
    Name='ProjectRockDB',
    Description='ProjectRock Variable referenced in Ansible Playbook',
    Value=MongoDB,
    Type='String',
    Overwrite=True,
    Tier='Standard'
    )