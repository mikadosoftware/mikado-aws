Running a SSL Static website on AWS
===================================

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

