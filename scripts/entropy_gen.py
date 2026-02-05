import os
import secrets
import string
import json
import argparse

def generate_secure_data(length=32, count=1):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    results = []
    
    for _ in range(count):
        data = ''.join(secrets.choice(alphabet) for i in range(length))
        results.append(data)
        
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate air-gapped desktop entropy.")
    parser.add_argument("--length", type=int, default=32)
    parser.add_argument("--count", type=int, default=1)
    args = parser.parse_args()
    
    secure_data = generate_secure_data(args.length, args.count)
    print(json.dumps({"entropy": secure_data}, indent=2))
