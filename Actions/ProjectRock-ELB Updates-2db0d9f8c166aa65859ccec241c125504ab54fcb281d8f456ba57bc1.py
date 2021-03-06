import boto3
def handler(context, inputs):
    #Originally had Demo working in AWS SIN & SYD Regions have changed demo to only work in SYD.  
    #Code kept same incase I change my mind in future
    
    SSLSingapore = "arn:aws:acm:ap-southeast-1:994172548385:certificate/3bae16ae-ac3f-4c42-bc79-5c114777e751"
    SSLSydney = "arn:aws:acm:ap-southeast-2:994172548385:certificate/c7f0a436-f494-4525-a566-fa1da31fc175"
        
    Region = str(inputs['customProperties']['Region'])
    Platform = str(inputs['customProperties']['Platform'])
    LBName = str(inputs['customProperties']['LBName'])
    print(LBName)
    if Platform == "platform:aws":
      if Region == "region:sydney":
          SSL = SSLSydney
          region_code = "ap-southeast-2"
      else:
          SSL = SSLSingapore
          region_code = "ap-southeast-1"
      print(region_code)
      client = boto3.client('elb', region_name=region_code)
      response = client.describe_load_balancers(LoadBalancerNames=[])
      elb = [elb['LoadBalancerName'] for elb in response['LoadBalancerDescriptions']]
      for x in elb:
         if LBName in x:
             print(x)
             response = client.create_load_balancer_listeners(
             LoadBalancerName = x,
             Listeners=[
                 {
                     'Protocol': 'https',
                     'LoadBalancerPort': 443,
                     'InstanceProtocol': 'http',
                     'InstancePort': 80,
                     'SSLCertificateId': SSL
                 },
             ]
             )
    outputs = {
    }
    return outputs