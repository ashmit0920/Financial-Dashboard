import redis
import yfinance as yf
import pickle
import zlib
import os
from dotenv import load_dotenv

# Initialize Redis client
load_dotenv()

HOST_URL = os.getenv('HOST_URL')
PASS = os.getenv('PASS')

redis_client = redis.Redis(
  host=HOST_URL,
  port=18625,
  password=PASS)

def get_stock_data(tickers, start_date, end_date):
    # Create a unique key for Redis
    key = f"{','.join(tickers)}_{start_date}_{end_date}"
    
    # Check if data is cached in Redis
    if redis_client.exists(key):
        # Get data from Redis
        cached_data = redis_client.get(key)
        # Decompress the data
        cached_df = pickle.loads(zlib.decompress(cached_data))
        return cached_df

    else:
        data = yf.download(tickers, start=start_date, end=end_date)
        # Cache the data in Redis for 24 hours
        redis_client.set(key, zlib.compress(pickle.dumps(data)))
        return data