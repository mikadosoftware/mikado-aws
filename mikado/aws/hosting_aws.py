"""
Hosting on AWS

https://docs.aws.amazon.com/AmazonS3/latest/user-guide/static-website-hosting.html

https://boto3.amazonaws.com/v1/documentation/api/1.9.42/guide/s3-example-creating-buckets.html

* open aws console
* unusual: yubikey failed (!)

Using boto
----------


S3
--

* AWS offers "S3 object lock" which prevents deletion, the idea is to enforce
customer retention periods usually for regulatory reasons.  Object lock set on
`create_bucket`.

route53
-------
setting up and controlling DNS 
set up A records for test.goodtechdad.com
hostedzone
https certificate?
https://www.freecodecamp.org/news/simple-site-hosting-with-amazon-s3-and-https-5e78017f482a/

"""
import os
import boto3
import botocore.exceptions
from mimetypes import MimeTypes
from pprint import pprint as pp

def get_s3_client():
    session = boto3.Session()
    client = session.client('s3')
    #s3 = session.resource('s3')
    return client

def list_buckets():
    """
    """
    s3 = get_s3_client()
    # Call S3 to list current buckets
    response = s3.list_buckets()
    # Get a list of all bucket names from the response
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    # Print out the bucket list
    print("Bucket List: %s" % buckets)

    try:
        result = s3.get_bucket_policy(Bucket='hackermews.org')
        print(result['Policy'])
    except botocore.exceptions.ClientError:
        print("no policy on that bucket")
        
    result = s3.get_bucket_acl(Bucket='hackermews.org')
    pp(result)

    print("###########################################")
    result = s3.get_bucket_website(Bucket='hackermews.org')
    pp(result)


def bucket_acls(name):
    s3 = get_s3_client()
    result = s3.get_bucket_acl(Bucket=name)
    pp(result)

    print("###########################################")
    result = s3.get_bucket_website(Bucket=name)
    pp(result)

def configure_bucket_for_webhost(name):
    """ 
    """
    # Define the website configuration
    website_configuration = {
        'ErrorDocument': {'Key': 'error.html'},
        'IndexDocument': {'Suffix': 'index.html'},
    }
    # Set the website configuration
    s3 = get_s3_client()
    s3.put_bucket_website(Bucket=name,
                          WebsiteConfiguration=website_configuration)
    
def add_bucket(name,
               region="us-west-1"):
    """
'EU'|'eu-west-1'|'us-west-1'|'us-west-2'|'ap-south-1'|'ap-southeast-1'|'ap-southeast-2'|'ap-northeast-1'|'sa-east-1'|'cn-north-1'|'eu-central-1'

ACL='private'|'public-read'|'public-read-write'|'authenticated-read',
    """
    s3 = get_s3_client()
    
    s3.create_bucket(Bucket=name,
                     ACL='public-read',
                     CreateBucketConfiguration={'LocationConstraint': region},
                     #GrantFullControl='string',
                     #GrantRead='string',
                     #GrantReadACP='string',
                     #GrantWrite='string',
                     #GrantWriteACP='string',
                     #ObjectLockEnabledForBucket=False
    )
    
def test_upload(name):
    s3 = get_s3_client()
    filename="index.html"
    s3.upload_file(filename, name, filename)
    
if __name__ == '__main__':
    #list_buckets()
    name='test.goodtechdad.com'
    #add_bucket(name)
    #configure_bucket_for_webhost(name)
    #
    #bucket_acls(name)
    test_upload(name)
