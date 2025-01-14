import dashboard.redis as redis
import json

# Connect to Redis
r = redis.Redis(host="192.168.121.48", port=6379, decode_responses=True)

# Fetch data from Redis
output_key = "gabrielbarros-proj3-output"
data = r.get(output_key)

if data:
    metrics = json.loads(data)
    print(metrics)
else:
    print("No data found in Redis!")
