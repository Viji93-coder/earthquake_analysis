import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector

# Global MySQL Connection
conn = mysql.connector.connect(
host="localhost",
user="root",
password="**********",
database="global"
)

def run_query(query):
    return pd.read_sql(query, conn)

# 1
def top_10_strongest():
    query="""(SELECT id, Country, mag, magnitude_flag, type
      FROM global_table 
      ORDER BY mag DESC LIMIT 10)"""
    return run_query(query)
    

#2 
def top_10_deepest():
    query="""(
    SELECT id,place,time,depth_km
    FROM global_table
    ORDER BY depth_km DESC
    LIMIT 10)"""
    return run_query(query)

# 3 
def  shallow_large():
    query="""(
    SELECT id,country,mag,depth_km
    FROM global_table
    WHERE depth_km < 50
    AND mag > 7.5
    ORDER BY mag DESC)"""
    return run_query(query)


# 5
def avg_magnitude():
    query="""(SELECT
    ROUND(AVG(mag),2) AS average_magnitude
    FROM global_table)"""
    return run_query(query)


# 6
def year_most_earthquake():
    query="""( SELECT year,type,
    COUNT(*) AS earthquake_count
    FROM global_table
    where type = 'earthquake'
    GROUP BY year
    ORDER BY earthquake_count DESC
    LIMIT 1)"""
    return run_query(query)

# 7
def month_most_earthquake():
    query="""( SELECT month,type
    COUNT(*) AS earthquake_count
    FROM global_table
    where type = 'earthquake'
    GROUP BY month ORDER BY earthquake_count DESC
    LIMIT 1)"""
    return run_query(query)


# 8
def day_most_earthquake():
    query="""(SELECT day_of_week AS day_name,type
    COUNT(*) AS earthquake_count
    FROM global_table
    where type = 'earthquake'
    GROUP BY day_name
    ORDER BY earthquake_count DESC
    LIMIT 1)"""
    return run_query(query)

#9
def hour_most_earthquake():
    query="""(SELECT hour,type
    COUNT(*) AS earthquake_count
    FROM global_table
    where type = 'earthquake'
    GROUP BY hour
    ORDER BY earthquake_count DESC
    LIMIT 1)"""
    return run_query(query)


# 10
def most_active_network():
    query="""(SELECT net,COUNT(*) AS earthquake_count
    FROM global_table
    GROUP BY net
    ORDER BY earthquake_count DESC
    LIMIT 1)"""
    return run_query(query)

# 11
def top_5_casualties():
    query="""( SELECT country,max(sig) AS max_significance
    FROM global_table
    GROUP BY country
    ORDER BY max_significance DESC
    LIMIT 5)"""
    return run_query(query)




# 13
def avg_loss_alert():
    query="""( SELECT alert,ROUND(AVG(POWER(mag,3) * sig),2) AS avg_estimated_Loss
    FROM global_table
    GROUP BY alert
    ORDER BY avg_estimated_loss DESC)"""
    return run_query(query)


# 14
def reviewed_vs_automatic():
    query="""( SELECT status,COUNT(*) AS earthquake_count
    FROM global_table
    GROUP BY status)"""
    return run_query(query)


# 15
def count_by_type():
    query="""(SElECT type,COUNT(*) AS earthquake_count
    FROM global_table
    GROUP BY type
    ORDER BY earthquake_count DESC)"""
    return run_query(query)


# 16
def count_by_data_type():
    query="""(SELECT types,COUNT(*) AS earthquake_count
    FROM global_table
    GROUP BY types
    ORDER BY earthquake_count DESC)"""
    return run_query(query)


# 18
def high_station_coverage():
    query="""( SELECT id,country,nst
    FROM global_table
    WHERE nst > 100
    ORDER BY nst DESC)"""
    return run_query(query)


# 19
def tsunami_per_year():
    query="""( SELECT  year,COUNT(*) AS tsunami_count
    FROM global_table
    WHERE tsunami = 1
    GROUP BY year
    ORDER BY year)"""
    return run_query(query)

# 20
def alert_level_count():
    query="""(SELECT alert,COUNT(*) AS earthquake_count
    FROM global_table
    GROUP BY alert
    ORDER BY earthquake_count DESC)"""
    return run_query(query)


# 21
def top_5_country_avg_mag():
    query="""(SELECT country,ROUND(AVG(mag),2) AS avg_magnitude
    FROM global_table
    GROUP BY country
    ORDER BY avg_magnitude DESC
    LIMIT 5)"""
    return run_query(query)


# 22
def shallow_deep_same_month():
    query="""(SELECT country,year,month,COUNT(DISTINCT depth_category) AS depth_types
    FROM global_table
    GROUP BY country, year,month
    HAVING COUNT(DISTINCT depth_km) >= 2)"""
    return run_query(query)


# 23
def yoy_growth():
    query="""( WITH yearly AS (
    SELECT  year,COUNT(*) AS earthquake_count
    FROM global_table
    GROUP BY YEAR(time))
    SELECT
    year,
    earthquake_count,
    ROUND((earthquake_count - LAG(earthquake_count) OVER(ORDER BY year)) * 100.0 / LAG(earthquake_count) OVER (ORDER BY year), 2 ) AS yoy_growth
    FROM yearly)"""
    return run_query(query)

# 24
def seismically_active_regions():
    query="""(SELECT place,COUNT(*) AS frequency,
    ROUND(AVG(mag),2) AS avg_magnitude,
    COUNT(*), AVG(mag) AS activity_score
    FROM global_table
    GROUP BY place
    ORDER BY activity_score DESC
    LIMIT 3)"""
    return run_query(query)


# 25
def equator_avg_depth():
    query="""(SELECT country,ROUND(AVG(depth_km),2) AS avg_depth
    FROM global_table
    WHERE latitude BETWEEN -5 AND 5
    GROUP BY country
    ORDER BY avg_depth DESC)"""
    return run_query(query)


# 26
def shallow_deep_ratio():
    query="""(SELECT country,SUM(CASE WHEN depth_category='shallow' THEN 1 ELSE 0 END) AS shallow_count,
    SUM(CASE WHEN depth_category='deep' THEN 1 ELSE 0 END) AS deep_count,
    ROUND(SUM(CASE WHEN depth_category='shallow' THEN 1 ELSE 0 END) /
    NULLIF(SUM(CASE WHEN depth_category='deep' THEN 1 ELSE 0 END),0),2) AS ratio
    FROM global_table
    GROUP BY country
    ORDER BY ratio DESC)"""
    return run_query(query)


# 27
def tsunami_magnitude_difference():
    query="""(SELECT tsunami,ROUND(AVG(mag),2) AS average_magnitude
    FROM global_table
    GROUP BY tsunami)"""
    return run_query(query)


# 28
def lowest_data_reliability():
    query="""(SELECT  id,country,rms,gap,(rms + gap) AS error_score
    FROM global_table
    ORDER BY error_score DESC
    LIMIT 20)"""
    return run_query(query)


# 30
def deep_focus_regions():
    query="""(  
    SELECT  country,COUNT(*) AS deep_quake_count
    FROM global_table
    WHERE depth_km > 300
    GROUP BY country
    ORDER BY deep_quake_count DESC)"""
    return run_query(query)

    

ANALYTICS = {
    "1. Top 10 Strongest Earthquakes": top_10_strongest,
    "2. Top 10 Deepest Earthquakes":top_10_deepest,
    "3. Shallow (<50km) and Mag >7.5": shallow_large,
    "5. Average Magnitude": avg_magnitude,
    "6. Year With Most Earthquakes": year_most_earthquake,
    "7. Month With Most Earthquakes": month_most_earthquake,
    "8. Day With Most Earthquakes": day_most_earthquake,
    "9. Count of earthquakes per hour of day" :hour_most_earthquake,
    "10. Most Active Network": most_active_network,
    "11. Top 5 Places With Highest Casualties":top_5_casualties,
    
    "13. Average Economic Loss By Alert Level": avg_loss_alert,
    "14. Reviewed vs Automatic Earthquakes": reviewed_vs_automatic,
    "15. Count By Earthquake Type": count_by_type,
    "16. Count By Data Type": count_by_data_type,
    
    "18. High Station Coverage Events": high_station_coverage,
    "19. Tsunami Count Per Year": tsunami_per_year,
    "20. Alert Level Count":alert_level_count,
    "21. Top 5 Countries By Average Magnitude": top_5_country_avg_mag,
    "22. Countries With Shallow And Deep Quakes": shallow_deep_same_month,
    "23. Year Over Year Growth": yoy_growth,
    "24. Most Seismically Active Regions": seismically_active_regions,
    "25. Equatorial Average Depth": equator_avg_depth,
    "26. Shallow To Deep Ratio": shallow_deep_ratio,
    "27. Tsunami Magnitude Difference": tsunami_magnitude_difference,
    "28. Lowest Data Reliability Events": lowest_data_reliability,
    "30. Deep Focus Regions": deep_focus_regions
}