#!/bin/env python
"""


https://docs.aws.amazon.com/AmazonS3/latest/dev/VirtualHosting.html

Example CNAME Method

This example uses www.johnsmith.net as the bucket name and homepage.html as the key name. To use this method, you must configure your DNS name as a CNAME alias for bucketname.s3.amazonaws.com.

The URL is as follows:

http://www.johnsmith.net/homepage.html
The example is as follows:

GET /homepage.html HTTP/1.1
Host: www.johnsmith.net

Err that only works for non ssl !!!!

https://medium.com/@sbuckpesch/setup-aws-s3-static-website-hosting-using-ssl-acm-34d41d32e394
https://www.freecodecamp.org/news/simple-site-hosting-with-amazon-s3-and-https-5e78017f482a/
https://medium.com/@channaly/how-to-host-static-website-with-https-using-amazon-s3-251434490c59

https://aws.amazon.com/premiumsupport/knowledge-center/cloudfront-https-requests-s3/
https://bryce.fisher-fleig.org/blog/setting-up-ssl-on-aws-cloudfront-and-s3/

From Bryce fisher:

We want to host static files on AWS S3.
Then have cloudfront do the https hand off and route via SNI

SNI - extension to TLS, allowing one IP address to server multiple hostnames (ie a header in the TLS call) - its HTTP1.1 virtual hosts but for SSL

1. Create S3 Bucket
- Adjust hosting to allow cloudfront to read it

{
  "Version":"2012-10-17",
  "Statement":[{
    "Sid":"PublicReadGetObject",
    "Effect":"Allow",
    "Principal": {
      "AWS": "*"
    },
    "Action":["s3:GetObject"],
    "Resource":["arn:aws:s3:::bryce-fisher-fleig-org/*"]
  }]
}

Letsencrypt
https://medium.com/@deepak13245/hosting-a-https-static-websites-using-s3-and-lets-encrypt-6f3e53014ff2
Need to set ARN in bucket

Getting a certificate
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client.request_certificate
Using boto ... :-)

Or use lets encrypt
https://medium.com/@e_99254/how-to-add-a-letsencrypt-certificate-to-a-site-hosted-on-s3-cloudfront-e22e13a36a45





"""
from pprint import pprint as pp
import boto3

class R53Zone():
    def __init__(self, d):
        """ingest data from `list_hosted_zones` """
        self.Id = d['Id']
        self.ResourceRecordSetCount = d['ResourceRecordSetCount']
        self.Config = d['Config']
        self.Name = d['Name']
    def __repr__(self):
        return "{}-{}".format(self.Name, self.ResourceRecordSetCount)
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
    
def get_r53_client():
    return boto3.client('route53')

def get_zones():
    zonesd = {}
    r53 = get_r53_client()
    _zones = r53.list_hosted_zones()
    for zone in _zones['HostedZones']:
        o = R53Zone(zone)
        print(o)
        zonesd[o.Name] = o
    return zonesd

if __name__ == '__main__':
    zonesd = get_zones()
    print(zonesd)
    #foo()
