"""Client that calls Inventory through the Kubernetes Service DNS name."""

import argparse
import json
import time
import urllib.request


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://inventory:8000/items/keyboard")
    parser.add_argument("--interval", type=float, default=1.0)
    args = parser.parse_args()
    print(f"client calling service URL: {args.url}", flush=True)
    while True:
        try:
            with urllib.request.urlopen(args.url, timeout=2) as response:
                body = json.loads(response.read())
                print(f"client response status={response.status} served_by={body.get('served_by')}", flush=True)
        except Exception as error:
            print(f"client request error={error}", flush=True)
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
