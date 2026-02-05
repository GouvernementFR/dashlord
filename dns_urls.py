from ipaddress import ip_address, ip_network

import dns.resolver

CLOUDFLARE_RANGES = [
    "173.245.48.0/20",
    "103.21.244.0/22",
    "103.22.200.0/22",
    "103.31.4.0/22",
    "141.101.64.0/18",
    "108.162.192.0/18",
    "190.93.240.0/20",
    "188.114.96.0/20",
    "197.234.240.0/22",
    "198.41.128.0/17",
    "162.158.0.0/15",
    "104.16.0.0/13",
    "104.24.0.0/14",
    "172.64.0.0/13",
    "131.0.72.0/22",
]

filename = "urls.txt"

with open(filename, encoding="utf-8") as file:
    urls = file.readlines()

cloudflare_urls = []
for url in urls:
    url = url.strip().replace("https://", "")
    ip_list = []
    try:
        answer = dns.resolver.resolve(url)
    except dns.resolver.NXDOMAIN:
        print(f"DNS failed: {url}")
        continue
    for data in answer:
        # check if the ip is in cloudflare ranges
        ip = data.to_text()
        if any(ip_address(ip) in ip_network(cidr) for cidr in CLOUDFLARE_RANGES):
            print(f"{url} is using Cloudflare DNS: {ip}")
            cloudflare_urls.append(url)

with open("cloudflare_urls.txt", "w", encoding="utf-8") as file:
    for url in set(cloudflare_urls):
        file.write(url + "\n")
