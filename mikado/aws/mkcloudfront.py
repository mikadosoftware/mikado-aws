#! /bin/env python
#! -*- coding:utf-8-*-

"""
Usng boto to crete cloundfront

First time - cloudfront and s3 no https, manually done

For cloundfront (a CDN with https support) we need to have an origin

S3:
  I think we have this automated already - create the S3 bucket and amend it
  config then upload something.


Cloudfront
THe bucket naming conventions - basically everything gets suffix

Origin Custom Headers: http headers that will be passed back
(not same as SNI)

make the DNS have a cname poiting to the cloudfront we just created
* http://test.goodtechdad.com/ - this gets a response from cloudfront, so the cname works but cloudfront says bad request

"""
from pprint import pprint as pp
import os
import boto3
from botocore.exceptions import ClientError
from mimetypes import MimeTypes

AMAZONSUFFIX = '.s3.amazonaws.com'
BUCKETNAME = 'test.goodtechdad.com' + AMAZONSUFFIX 
DNSNAME = 'test.goodtechdad.com'

def get_client(clienttype='cloudfront'):
    session = boto3.Session()
    client = session.client(clienttype)
    return client

def stackoverflow():
    cf = get_client()
    
    cf.create_distribution(DistributionConfig=dict(CallerReference='firstOne',
            Aliases = dict(Quantity=1, Items=[DNSNAME]),
            DefaultRootObject='index.html',
            Comment='Test distribution',
            Enabled=True,
            Origins = dict(
                Quantity = 1, 
                Items = [dict(
                    Id = '1',
                    DomainName=BUCKETNAME,
                    S3OriginConfig = dict(OriginAccessIdentity = ''))
                ]),
            DefaultCacheBehavior = dict(
                TargetOriginId = '1',
                ViewerProtocolPolicy= 'redirect-to-https',
                TrustedSigners = dict(Quantity=0, Enabled=False),
                ForwardedValues=dict(
                    Cookies = {'Forward':'all'},
                    Headers = dict(Quantity=0),
                    QueryString=False,
                    QueryStringCacheKeys= dict(Quantity=0),
                    ),
                MinTTL=1000)
            )
    )
    
def list_distributions():
    cf = get_client()
    res = cf.list_distributions()
    pp(res)

def run():
#    stackoverflow()
    list_distributions()
    
if __name__ == '__main__':
    run()
