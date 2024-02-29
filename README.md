# Climate Analysis and Flask App
This project involves analyzing climate data using Python, SQLAlchemy, Pandas, and Matplotlib. The data is stored in an SQLite database, and the analysis includes precipitation and station analysis.

## Part 1: Climate Analysis
1. Connect to the Database:/
  * Use SQLAlchemy to create an engine and reflect tables into classes (station and measurement).
  * Link Python to the database by creating a SQLAlchemy session.

2. Precipitation Analysis:/
  * Find the most recent date in the dataset.
  * Retrieve the previous 12 months of precipitation data.
  * Load the data into a Pandas DataFrame, sort by date, and plot the results.
  * Print summary statistics for the precipitation data.

3. Station Analysis:/
  * Calculate the total number of stations in the dataset.
  * Identify the most-active station and its observation counts.
  * Calculate the lowest, highest, and average temperatures for the most-active station.
  * Query the last 12 months of temperature observation (TOBS) data for the most-active station and plot as a histogram.

## Part 2: Climate App with Flask
Create a Flask API based on the analysis:

1.Homepage:/
  * Welcome message and list of available routes.

2. List of Routes:/
  * /api/v1.0/precipitation: Return JSON representation of the last 12 months of precipitation data.
  * /api/v1.0/stations: Return JSON list of stations.
  * /api/v1.0/tobs: Return JSON list of temperature observations for the most-active station in the previous year.
  * /api/v1.0/<start>: Return JSON list of TMIN, TAVG, and TMAX for dates greater than or equal to the specified start date.
  * /api/v1.0/<start>/<end>: Return JSON list of TMIN, TAVG, and TMAX for dates between the specified start and end dates.
