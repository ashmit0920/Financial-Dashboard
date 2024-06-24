# Financial Data Visualization Dashboard

## Overview

This project is a Financial Data Visualization Dashboard built using Dash, Plotly and Python. It allows users to visualize stock prices, moving averages, and trading volumes over a specified date range for multiple ticker symbols.

![User Interface](./User%20Interface.png)

## Features

- **Dynamic Visualization:** Display stock prices and moving averages (20-day, 50-day, 100-day) dynamically on a plot.
- **Interactive Controls:** Select ticker symbols, date range, and additional features (like trading volume) via user-friendly controls.
- **Redis Caching:** Utilizes Redis for caching downloaded stock data, reducing data retrieval time and improving application responsiveness.
- **Responsive Design:** Designed using Dash framework for responsive UI across different devices.
- **Dark Mode:** Uses Plotly's dark theme for enhanced visualization experience.

## Setup

Installation:
```
git clone https://github.com/ashmit0920/Financial-Dashboard.git
```
```
pip install -r requirements.txt
```

Run Redis Server: Start Redis server locally or configure connection details in a .env file (used in redis_cache.py). Type ```redis-server``` command in your terminal.

Run the Application: Start the Dash app by running app.py.
```
python app.py
```

Access Dashboard: Open a web browser and navigate to http://127.0.0.1:8050/ to view the dashboard.

## Redis Caching

- **Purpose:** Redis is used to cache stock market data retrieved from Yahoo Finance to optimize performance.
- **Implementation:** The redis_cache.py module initializes a Redis client, handles data caching, and ensures cached data integrity.
- **Benefits:** Reduces data retrieval time by serving cached data for repeated queries within a specified cache period (24 hours in this project).

## Future Updates

- **User Authentication:** Implement user authentication to personalize dashboard settings and save preferences.
- **Real-Time Data Updates:** Integrate WebSocket or API for real-time stock price updates.
- **Advanced Analytics:** Add statistical analysis tools like Sharpe Ratio calculation or correlation analysis.
- **Enhanced Visualization:** Expand visualization options with different chart types (e.g., candlestick charts) and technical indicators.