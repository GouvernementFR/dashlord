import requests

filename = "urls.txt"

with open(filename, encoding="utf-8") as file:
    urls = file.readlines()

for url in urls:
    url = url.strip()
    try:
        requests.get(url, timeout=15)
    except requests.RequestException as e:
        if "NameResolutionError" in str(e):
            print(f"DNS failed: {url}")
            try:
                # Test with www prefix
                requests.get(url.replace("://", "://www."), timeout=15)
                print(f"Rename URL: {url}\n")
                with open(filename, encoding="utf-8") as file:
                    lines = file.readlines()
                with open(filename, "w", encoding="utf-8") as file:
                    for line in lines:
                        if line.strip() == url:
                            line = line.replace(url, url.replace("://", "://www."))
                        file.write(line)
            except requests.RequestException:
                print(f"Delete URL: {url}\n")
                with open(filename, encoding="utf-8") as file:
                    lines = file.readlines()
                with open(filename, "w", encoding="utf-8") as file:
                    for line in lines:
                        if line.strip() != url:
                            file.write(line)
        else:
            print(f"Error accessing {url}")
            print(e, "\n")
