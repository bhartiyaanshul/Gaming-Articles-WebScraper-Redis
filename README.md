readme_content = """
Gaming Artciles WebScraper Redis

## Overview

This Python script utilizes Selenium for web scraping, Redis for data storage, and ChromeDriver for browsing. It extracts article details from a gaming website, writes the data to a local text file, and simultaneously stores the information in Redis with a 3-day expiration.

## Prerequisites

Make sure you have the following installed:

- Python 3.x
- Chrome browser
- ChromeDriver
- Redis server

You can install Python dependencies using:

```bash
pip install selenium webdriver_manager redis
