Running a SSL Static website on AWS
===================================


How to build Docker for AWS

https://packer.io/intro/getting-started/build-image.html



This will be a two-part manual.  The first part is to simply put a
static website onto AWS behind SSL/TLS.  Then I shall transition to a
dynamic webservice that uses the full stack of SDLC features.

This will hopefully form the basis to launch a simple SaaS business.



1. Create S3 Bucket

2. Create CloudFront Distrubtion

3. Get SSL Certificate
   a. Letsencrypt / Certificate Manager
   b. Generate private key / CSR
   c. Upload CSR to registry
   d. Validate (through DNS txt!)
   e. upload cert of AWS IAM
   

Buckets
-------
We cn create buckets automatically
Then we need to get the endpoint url
We can manuly do this by goign to S3 and lookng at the dialog box fro "static website hosting" - Endpoint : http://test.goodtechdad.com.s3-website-us-west-1.amazonaws.com
There presumably is an automated means
https://aws.amazon.com/premiumsupport/knowledge-center/cloudfront-serve-static-website/

when creating a cloudfront we yse that above endpoint


Getting a HTTPS Certificate
===========================

Let's Encrypt is an excellent provider of free, automated certificates.
But to get one, we need to demonstrate to LetsEncrypt we control the
domain we are needing a certificate for.

The way we shall do this is to put a LetsEncrypt provided GUID into the
TXT record of our Route53 hosted DNS.

Then we shall use certbot to generate the certificates.  At which point we can
investigate them and then upload to AWS to be part of our front end.


Being able to update a DNS TXT record
-------------------------------------

My route53-handler is frigged to be able to upsert a TXT record.
I will use this

https://serverfault.com/questions/750902/how-to-use-lets-encrypt-dns-challenge-validation

certbot -d www.iapprove.net --manual --preferred-challenges dns certonly


Please deploy a DNS TXT record under the name
_acme-challenge.www.iapprove.net with the following value:

D8yXRY3EbeKiq7p2mROqutXxFI64z5YJDodfN1N4pLE

Before continuing, verify the record is deployed.



hallenges
Failed authorization procedure. www.iapprove.net (dns-01): urn:ietf:params:acme:error:dns :: DNS problem: NXDOMAIN looking up TXT for _acme-challenge.www.iapprove.net - check that a DNS record exists for this domain

IMPORTANT NOTES:
 - The following errors were reported by the server:

   Domain: www.iapprove.net
   Type:   None
   Detail: DNS problem: NXDOMAIN looking up TXT for
   _acme-challenge.www.iapprove.net - check that a DNS record exists
   for this domain
 - Your account credentials have been saved in your Certbot
   configuration directory at /etc/letsencrypt. You should make a
   secure backup of this folder now. This configura
