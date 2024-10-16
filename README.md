**README: Perceived Energy Score - Data Aggregation Solution**

**Overview**
This project aims to build a MongoDB aggregation pipeline to generate a Perceived Energy Score for users based on their mood, activity, and sleep data, fetched from sources like Google Fit, Fitbit, and Apple Watch. The objective is to fetch all relevant data of users who have been active on a certain day and aggregate their mood scores, activity metrics (steps, active minutes), and sleep data.

**Problem Statement**
A Product Manager at Wysa would like to introduce a Perceived Energy Score service. To compute this score, we need to:

1. Analyze the user's mood check-in (mood score).
2. Evaluate their level of activity (steps/active minutes).
3. Retrieve their sleep data from external health monitoring devices (Google Fit/Fitbit/Apple Watch).

**The solution should involve the following:**

1. Use a MongoDB aggregation pipeline to fetch mood score, activity, and sleep data for users who have been active on a given day.
2. Develop a batch process to extract, transform, and aggregate the data, and write the result to a JSON file.

**Key MongoDB Collections**
1. **User Collection**
The users collection contains basic user profile information such as username, timezone, and app version.

2. **Mood Score Collection**
The mood_score collection tracks the user's mood over time. Each document captures a mood score (on a scale from 1-10) and the timestamp of the check-in

3. **Activity Collection**
The activities collection stores activity data such as steps, duration, calories, etc. 

4. **Sleep Collection**
The sleep collection stores sleep data, including sleep score, hours of sleep, and hours in bed

**MongoDB Aggregation Pipeline**
To fetch mood score, activity, and sleep data of active users on a given day, the MongoDB aggregation pipeline will:

1. **Filter users by active day**: Check for mood, activity, or sleep data on the target day.
2. **Group data** by user ID and day.
3. **Aggregate mood scores, activity logs, and sleep data** for each user.

**Batch Process**
The batch process is responsible for extracting the data, transforming it using the aggregation pipeline, and writing the results to a JSON file.

Steps:
1. **Extract:** Fetch data using the MongoDB aggregation pipeline for users active on a given day.
2. **Transform:** Aggregate mood score, activity, and sleep data into a summarized format for each user.
3. **Write to JSON:** Save the aggregated results to a JSON file for further processing or reporting.

**Project Structure**
**The following folder structure organizes the data and response screenshots:**

**data/:**
Contains sample user data, mood scores, activity logs, and sleep metrics used in the aggregation pipeline.

**responses/:**
Contains screenshots of responses from MongoDB queries and aggregation pipeline outputs.

**Running the Project**

**Prerequisites**
Ensure the following software is installed:

**MongoDB** (with access to collections mentioned above)
**Python** (3.x)
**Virtualenv** (optional for virtual environment)
**Required Python packages** (e.g.,flask, pymongo for MongoDB interaction)

**Resources**

The responses/ folder includes screenshots of the MongoDB query responses and the aggregation pipeline results.

The data/ folder contains sample data for testing and demonstration purposes.


This project successfully fetches mood, activity, and sleep data for active users on a given day using MongoDB's aggregation pipeline and provides a batch process to extract and write the data to a JSON file. This lays the groundwork for computing the Perceived Energy Score.
