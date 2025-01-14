import streamlit as st
import dashboard.redis as redis
import json
import pandas as pd

# Connect to Redis
redis_host = "192.168.121.48"
redis_port = 6379
r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

# Fetch data from Redis
output_key = "ifs4-proj3-output"
data = r.get(output_key)

st.title("Monitoring Dashboard")
st.markdown("This dashboard displays metrics computed by the serverless function.")

if data:
    metrics = json.loads(data)

    # Display metrics as a table
    df = pd.DataFrame([metrics])
    st.dataframe(df)

    # Plot metrics
    st.subheader("CPU Utilization (Moving Average)")
    cpu_metrics = {k: v for k, v in metrics.items() if k.startswith("avg-util-cpu")}
    st.bar_chart(pd.Series(cpu_metrics))

    st.subheader("Network and Memory Usage")
    st.metric("Network Egress (%)", metrics["percent-network-egress"])
    st.metric("Memory Cache (%)", metrics["percent-memory-cache"])
else:
    st.error("No data found in Redis! Ensure the serverless function is running.")
