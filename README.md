First Alpha - For Educational Purpose Only
==================================================
This tool will help you to automate adding blocked domain by [DNS Nawala](http://nawala.org) to the hosts file.

## How it works
1. Program will run in daemon mode, and act as DNS server, so user need to change DNS server to localhost (127.0.0.1)
2. When user request a domain, the program will forward the request to Nawala, if the return address is 114.127.223.16 (CHECK) then the domain is blocked.
3. The program then request the actual address using [DNS over REST](http://dig.jsondns.org/) and added it to hosts file.
4. That's it!

## Getting started
1. Change your DNS Server to localhost, *nix environment is located in /etc/resolv.conf
<pre>nameserver 127.0.0.1</pre>
2. Run it (need to be root)
<pre>$ sudo python anti-nawala.py</pre>

## Limitation
User needs to compile/ install the program, and it's only works for localhost. Still need to figure a way to use it as SaS/ Cloud.

## Other DNS Filtering
This program might work as well for other DNS filtering like OpenDNS, but we need to know the characteristic from it, for example nawala will return address 114.127.223.16 (CHECK) if the domain is blocked.


