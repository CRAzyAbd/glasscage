from mitmproxy import http
import logging

# Mitmproxy uses its own logging system
logging.basicConfig(level=logging.INFO)

class C2Tracker:
    def request(self, flow: http.HTTPFlow):
        # Extract the destination URL and HTTP method
        url = flow.request.pretty_url
        method = flow.request.method
        
        # Log the intercepted traffic
        print(f"\n[!] ALERT - Outbound Traffic Intercepted:")
        print(f"    Method: {method}")
        print(f"    Target: {url}")

# Register the addon with mitmproxy
addons = [C2Tracker()]