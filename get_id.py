import time

def generate_customer_id():
    # Get the current timestamp in microseconds
    timestamp = int(time.time() * 100)
    return str(timestamp)

# Generate and print the customer ID
print(generate_customer_id())