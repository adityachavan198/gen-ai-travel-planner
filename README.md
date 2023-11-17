# gen-ai-travel-planner

Travel Itinerary Generator
This is a simple Travel Itinerary Generator using Streamlit and the Google PaLM model for text generation. The app takes user input, such as the city to visit, the number of days for the trip, and user preferences for activities, and generates a personalized itinerary.

Prerequisites
Before running the app, make sure you have the required dependencies installed. You can install them using the following command:


pip install streamlit google.generativeai
Getting Started
Clone this repository to your local machine:

git clone https://github.com/adityachavan198/gen-ai-travel-planner
Change to the project directory:

cd gen-ai-travel-planner
Set up your Palm API key:
Obtain an API key from Google.
Set the API key as an environment variable. You can do this in your terminal:

export PALM_API_KEY="your-api-key"
Run the Streamlit app:

streamlit run app.py
Open your web browser and go to http://localhost:8501 to access the app.
Usage
Enter the city you're visiting and the number of days for your trip.
Check the preferences for activities you're interested in.
Click the "Generate Itinerary" button to get a personalized itinerary.
Contributing
Feel free to contribute to the development of this project by opening issues or submitting pull requests.