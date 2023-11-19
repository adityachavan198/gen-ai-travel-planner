import streamlit as st
from ics import Calendar, Event
from datetime import datetime, timedelta
import json

# Streamlit app title
st.title("Calendar Export Tester")

# Itinerary JSON string
itinerary_json_string = """
{
  "days": [
    {
      "day": 1,
      "activities": [
        {
          "title": "Central Park",
          "description": "Explore Central Park, one of New York City's most iconic landmarks. Enjoy a leisurely stroll through the park's lush green lawns, visit the Central Park Zoo, or take a ride in the Central Park Carousel.",
          "link": "https://www.centralparknyc.org/",
          "start_time": "10:00 AM",
          "end_time": "12:00 PM",
          "location": "Central Park"
        },
        {
          "title": "The High Line",
          "description": "Take a walk or bike ride along the High Line, a former elevated railway that has been transformed into a public park. Enjoy stunning views of the city skyline and stop to admire the unique art installations that line the path.",
          "link": "https://www.thehighline.org/",
          "start_time": "02:00 PM",
          "end_time": "04:00 PM",
          "location": "The High Line"
        }
      ]
    },
    {
      "day": 2,
      "activities": [
        {
          "title": "Brooklyn Bridge Park",
          "description": "Enjoy stunning views of the Manhattan skyline from Brooklyn Bridge Park. Take a walk or bike ride along the waterfront, visit the Brooklyn Museum, or catch a free concert at the Pier 6 Concert Pavilion.",
          "link": "https://www.brooklynbridgepark.org/",
          "start_time": "09:30 AM",
          "end_time": "11:30 AM",
          "location": "Brooklyn Bridge Park"
        },
        {
          "title": "Prospect Park",
          "description": "Explore Prospect Park, Brooklyn's largest park. Enjoy a picnic in the park's meadows, visit the Prospect Park Zoo, or take a hike in the park's wooded hills.",
          "link": "https://www.prospectpark.org/",
          "start_time": "01:00 PM",
          "end_time": "03:00 PM",
          "location": "Prospect Park"
        }
      ]
    }
  ]
}
"""

# Convert JSON string to dictionary
itinerary_json = json.loads(itinerary_json_string)

# Print the loaded itinerary_json for debugging
print("Loaded itinerary_json:", itinerary_json)

def get_download_link(content, filename):
    """Generates a download link for the given content."""
    b64_content = content.encode().decode("utf-8")
    href = f'<a href="data:text/calendar;charset=utf-8,{b64_content}" download="{filename}">Download {filename}</a>'
    return href


# Export to calendar button
if st.button("Export to Calendar"):
    print("export")
    cal = Calendar()
    start_date = datetime.now() + timedelta(days=1)

    for day, activities in enumerate(itinerary_json.get("days", []), start=1):
        for activity in activities.get("activities", []):
            event = Event()
            event.name = activity.get("title", "")
            event.description = activity.get("description", "")
            event.location = activity.get("location", "")
            event.begin = start_date + timedelta(days=day - 1, hours=int(activity.get("start_time", "00:00").split(":")[0]), minutes=int(activity.get("start_time", "00:00").split(":")[1][:2]))
            event.end = start_date + timedelta(days=day - 1, hours=int(activity.get("end_time", "00:00").split(":")[0]), minutes=int(activity.get("end_time", "00:00").split(":")[1][:2]))
            cal.events.add(event)

    cal_content = str(cal)  # Use __str__ to obtain the serialized iCalendar content

    # Create a download link
    st.success("Calendar file exported!")
    st.markdown(get_download_link(cal_content, "Itinerary.ics"), unsafe_allow_html=True)
