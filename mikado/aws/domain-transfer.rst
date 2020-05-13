

I want to transfer all my domans to route53 and manage them all with
boto-enabled scripts.  I find registrars a bit awkward to do a domain
transfer - sometimes for good protecting me from identity theft
reasons, and also keeping my annual fees coming in.


Easily.co.uk
------------
(See article on goodbye easily)

We can dive into their new domain manager and there is "Transfer Out button"
On a low impact domain, I have clicked and been given an EPP code by email


Process
-------

1. Migrate the DNS service (ie the name server) to ROute53 *first*. Else your old provider might switch it off
(https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/migrate-dns-domain-in-use.html)

Topics

Step 1: Get Your Current DNS Configuration from the Current DNS Service Provider (Optional but Recommended)
Step 2: Create a Hosted Zone
Step 3: Create Records
Step 4: Lower TTL Settings
Step 5: Wait for the Old TTL to Expire
Step 6: Update the NS Record with Your Current DNS Service Provider to Use Route 53 Name Servers
Step 7: Monitor Traffic for the Domain
Step 8: Update the Domain Registration to Use Amazon Route 53 Name Servers
Step 9: Change the TTL for the NS Record Back to a Higher Value
Step 10: Transfer Domain Registration to Amazon Route 53


Or easier method


Step 1: Get Your Current DNS Configuration from the Current DNS Service Provider (Inactive Domains)
Step 2: Create a Hosted Zone (Inactive Domains)
Step 3: Create Records (Inactive Domains)
Step 4: Update the Domain Registration to Use Amazon Route 53 Name Servers (Inactive Domains)



2. 

Biblio
------
https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/domain-transfer-to-route-53.html

https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/MigratingDNS.html


name.com
