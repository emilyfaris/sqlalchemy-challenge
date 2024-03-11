# sqlalchemy-challenge

## Overview

This project involves performing climate analysis and data exploration of a climate database using Python, SQLAlchemy ORM, Pandas, and Matplotlib. The goal is to use data engineering techniques to analyze climate patterns and design a Flask API to serve the analysis results.

## Technologies Used

- Python
- SQLAlchemy ORM
- Pandas
- Matplotlib
- Flask

## Database Analysis

The climate database consists of temperature and precipitation data. Using SQLAlchemy ORM queries, the analysis explores temperature trends, precipitation levels, and station activity within the dataset. The exploration involves:

- Precipitation analysis over the last 12 months of the dataset.
- Station analysis to find the most active stations and observe temperature trends.
- Temperature analysis for the most active station over the last year.

### Precipitation Analysis

A query was designed to retrieve the last 12 months of precipitation data, plotted to visualize trends and examine changes over time.

### Station Analysis

Analysis identified the station with the highest number of observations. Temperature observation data (TOBS) for the last 12 months of this station was also retrieved and plotted as a histogram.

## Flask API Design

Following the analysis, a Flask API was developed to serve the results. The API provides endpoints for accessing the analysis data, including:

- `/`: The homepage lists all available API routes.
- `/api/v1.0/precipitation`: Returns the last 12 months of precipitation data.
- `/api/v1.0/stations`: Lists all stations from the dataset.
- `/api/v1.0/tobs`: Shows the temperature observations of the most active station for the last 12 months.
- `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`: Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.


