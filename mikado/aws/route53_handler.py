#!/bin/env python
"""


https://danieljamesscott.org/17-software/development/33-manipulating-aws-route53-entries-using-boto.html

https://docs.aws.amazon.com/AmazonS3/latest/dev/VirtualHosting.html

Example CNAME Method

This example uses www.johnsmith.net as the bucket name and
homepage.html as the key name. To use this method, you must configure
your DNS name as a CNAME alias for bucketname.s3.amazonaws.com.

The URL is as follows:

http://www.johnsmith.net/homepage.html
The example is as follows:

GET /homepage.html HTTP/1.1
Host: www.johnsmith.net

Err that only works for non ssl !!!!


https://bryce.fisher-fleig.org/blog/setting-up-ssl-on-aws-cloudfront-and-s3/

From Bryce fisher:

We want to host static files on AWS S3.
Then have cloudfront do the https hand off and route via SNI

SNI - extension to TLS, allowing one IP address to server multiple hostnames (ie a header in the TLS call) - its HTTP1.1 virtual hosts but for SSL



"""
from pprint import pprint as pp
import boto3

def get_r53_client():
    return boto3.client('route53')


class R53Zone():
    def __init__(self, d):
        """ingest data from `list_hosted_zones` """
        self.Id = d['Id']
        self.ResourceRecordSetCount = d['ResourceRecordSetCount']
        self.Config = d['Config']
        self.Name = d['Name']
        ### fill out RRS
        r53 = get_r53_client()
        self.rrs = r53.list_resource_record_sets(HostedZoneId=self.Id)

    def __repr__(self):
        return "{}-{} RRS".format(self.Name, self.ResourceRecordSetCount)
    def fetch_zone(self):
        """Retireve the data about me """
        pass
    
def foo():
    name = 'cleanpython.com.'
    Id = '/hostedzone/Z37ZH240XSI8D6'
    r53 = get_r53_client()
    zone = r53.get_hosted_zone(Id=Id)
    pp(zone)
    rrs = r53.list_resource_record_sets(HostedZoneId=Id)
    pp(rrs['ResourceRecordSets'])
    

def get_zones():
    zonesd = {}
    r53 = get_r53_client()
    _zones = r53.list_hosted_zones()
    for zone in _zones['HostedZones']:
        
        o = R53Zone(zone)
        print(o)
        zonesd[o.Name] = o
    return zonesd

def get_this_zone(domainname):
    print("Get Zone")
    if not domainname.endswith('.'):
        domainname = domainname + "."
    # we assume good entry data - ie that we own this.
    
    r53 = get_r53_client()
    _zones = r53.list_hosted_zones()
    o = None
    for zone in _zones['HostedZones']:
        
        print(zone['Name'],'wibble' )
        if zone['Name'] == domainname:
            o = R53Zone(zone)
    return o

### change - add txt
#
def mk_change_request(hostedZoneId):
    """ """
    change = {
        'Comment': 'COmment1',
        'Changes': [
            {
                'Action':'UPSERT',
                'ResourceRecordSet': {
                    'Name': '_acme-challenge.www.iapprove.net.',
                    'Type': 'TXT',
                    'TTL': 300,
                    'ResourceRecords': [
                        {
                            'Value': '"T_eipjPzxqyIaCXG4EvPfgIm463G5Nqr9ukZA8aw3pw"',
                        },
                    ],
#                    'AliasTarget': {
#                        'HostedZoneId': hostedZoneId,
#                        'DNSName': 'iapprove.net.',
#                        'EvaluateTargetHealth': False
#                    },
                  }
            },
        ]
    }
    #response = client.change_resource_record_sets(
    
    #return change
    r53 = get_r53_client()
    results = r53.change_resource_record_sets(
           HostedZoneId=hostedZoneId,
           ChangeBatch=change)
    pp(results)
   # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.change_resource_record_sets
    error='''An error occurred (InvalidInput) when calling the ChangeResourceRecordSets operation: Invalid request: 
    Expected exactly one of 
      [AliasTarget, 
      all of [TTL, and ResourceRecords], 
     or TrafficPolicyInstanceId], 
         but found none in Change with [Action=UPSERT, Name=iapprove.net., 
           Type=TXT, SetIdentifier=null] '''

    
if __name__ == '__main__':
    #zonesd = get_zones()
    #print(zonesd)
    o = get_this_zone('iapprove.net')
    pp(o.rrs)
    print(o.Id)
    #mk_change_request(o.Id)


    # The process is to run certbot - and it pauses while I update records.
    # but it is not clear how much time route53 needs after I chaange the
    # record cos I tested it with XXX, and few minutes later I reran
    # and xxx was still in whatever certbot reached out to.
    #
    # So we want to get a valid certificate for a domain name.
    # we will use certbot to get one from LetsEncrypt

    #$ sudo certbot -d www.iapprove.net --manual --preferred-challenges dns certonly

    # THis is asking for a cert for www.iapprove.net.  THis is my test domain

    # once I have this down I will try and get it working autoamtically for
    # other domains and just host things.

    # so the delay was arounf 3 minutes.
    # I now have a .pem file
    
"""
IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/www.iapprove.net/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/www.iapprove.net/privkey.pem
   Your cert will expire on 2020-05-24. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot
   again. To non-interactively renew *all* of your certificates, run
   "certbot renew"
"""
