#!/bin/env python
"""
library module providing basic route53 features via boto

TODO: why am I sometimes got ns and sometimss not - how do i create DNS properly
for a zone, and then do txt cert and then how do I get it on AWS / S3

Then how do I host a dynamic web server on AWS/

THen use KMS form AWS?

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
    zonesd = get_zones()
    pp(zonesd)
    import sys; sys.exit()
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
