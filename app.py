import streamlit as st
import pprint
import google.generativeai as palm
import os
from ics import Calendar, Event
from datetime import datetime, timedelta
import json

palm.configure(api_key=os.getenv("PALM_API_KEY"))
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name
print(model)

# Streamlit app title and user input
st.title("Travel Itinerary Generator")

city = st.text_input("Enter the city you're visiting:")
start_date = st.date_input("Select the start date for your trip:", value=datetime.today())

# Set the maximum end date to 30 days after the start date
max_end_date = start_date + timedelta(days=30)

# User selects the end date of the trip
end_date = st.date_input("Select the end date for your trip:", 
                         value=start_date + timedelta(days=1),  # Default to the next day
                         min_value=start_date, 
                         max_value=max_end_date)

# Calculate the number of days between start_date and end_date
days = (end_date - start_date).days
#days = st.number_input("Enter the number of days for your trip:", min_value=1, max_value=30)

# User preferences checkboxes
art = st.checkbox("Art")
museums = st.checkbox("Museums")
outdoor = st.checkbox("Outdoor Activities")
indoor = st.checkbox("Indoor Activities")
kids_friendly = st.checkbox("Good for Kids")
young_people = st.checkbox("Good for Young People")

# Generate itinerary button
if st.button("Generate Itinerary"):
    # Create a prompt based on user input
    
    prompt = f"You are an travel expert. Give me an itenary for {city}, for {days} days, assume each day starting at 10am and ending at 8pm having a buffer of 30 minutes between each activity. I like to"
    if art:
        prompt += " explore art,"
    if museums:
        prompt += " visit museums,"
    if outdoor:
        prompt += " engage in outdoor activities,"
    if indoor:
        prompt += " explore indoor activities,"
    if kids_friendly:
        prompt += " find places suitable for kids,"
    if young_people:
        prompt += " discover places suitable for young people,"

    # prompt += ". Return the response in a properly formatted json string which can be imported in code using json.loads function in python."
    prompt += """Limit the length of output json string to 1200 characters. Generate a structured JSON representation for the travel itinerary.

       {
  "days": [
    {
      "day": 1,
      "activities": [
        {
          "title": "Activity 1",
          "description": "Description of Activity 1",
          "link": "https://example.com/activity1",
          "start_time": "10:00 AM",
          "end_time": "12:00 PM",
          "location": "https://maps.google.com/?q=location1"
        },
        {
          "title": "Activity 2",
          "description": "Description of Activity 2",
          "link": "https://example.com/activity2",
          "start_time": "02:00 PM",
          "end_time": "04:00 PM",
          "location": "https://maps.google.com/?q=location2"
        },
        ....
      ]
    },
    {
      "day": 2,
      "activities": [
        {
          "title": "Another Activity 1",
          "description": "Description of Another Activity 1",
          "start_time": "09:30 AM",
          "end_time": "11:30 AM",
          "location": "https://maps.google.com/?q=location1"
        },
        {
          "title": "Another Activity 2",
          "description": "Description of Another Activity 2",
          "start_time": "01:00 PM",
          "end_time": "03:00 PM",
          "location": "https://maps.google.com/?q=location2"
        },
        ...
      ]
    }
  ]
}

        Ensure that each day has a 'day' field and a list of 'activities' with 'title', 'description', 'start_time', 'end_time', and 'location' fields. Keep descriptions concise.
"""

    # Call the OpenAI API
    completion = palm.generate_text(
    model=model,
    prompt=prompt,
    temperature=0,
    # The maximum length of the response
    max_output_tokens=3000,
)

    # Extract and display the generated itinerary
    itinerary = completion.result.strip()
    itinerary = itinerary[7:-3]
    # Display the itinerary from the JSON response
    print(type(itinerary))
    print(len(itinerary))
    print(itinerary)

    itinerary_json = json.loads(itinerary)

    for day in itinerary_json["days"]:
        st.header(f"Day {day['day']}")
        for activity in day["activities"]:
            st.subheader(activity["title"])
            st.write(f"Description: {activity['description']}")
            st.write(f"Location: {activity['location']}")
            st.write(f"Time: {activity['start_time']} - {activity['end_time']}")
            st.write(f"Link: {activity['link']}")
            st.write("\n")
    
    # Set the start date to tomorrow
    start_date = datetime.now() + timedelta(days=1)
    def get_download_link(content, filename):
        """Generates a download link for the given content."""
        b64_content = content.encode().decode("utf-8")
        href = f'<a href="data:text/calendar;charset=utf-8,{b64_content}" download="{filename}">Download {filename}</a>'
        return href
        print("export")

    cal = Calendar()
    start_date = datetime.now() + timedelta(days=10)

    for day, activities in enumerate(itinerary_json.get("days", []), start=1):
        for activity in activities.get("activities", []):
            event = Event()
            event.name = activity.get("title", "")
            event.description = activity.get("description", "")
            event.location = activity.get("location", "")
            print(event.location)
            print("start_date:", start_date)
            print("end_time:", start_date + timedelta(days=day - 1, hours=int(activity.get("end_time", "00:00").split(":")[0]), minutes=int(activity.get("end_time", "00:00").split(":")[1][:2])))
            event.begin = start_date + timedelta(days=day - 1, hours=int(activity.get("start_time", "00:00").split(":")[0]), minutes=int(activity.get("start_time", "00:00").split(":")[1][:2]))
            event.end = start_date + timedelta(days=day - 1, hours=int(activity.get("end_time", "00:00").split(":")[0]), minutes=int(activity.get("end_time", "00:00").split(":")[1][:2]))
            cal.events.add(event)

    cal_content = str(cal)  # Use __str__ to obtain the serialized iCalendar content

    # Create a download link
    st.success("Itinerary ready to export!")
    st.markdown(get_download_link(cal_content, "Itinerary.ics"), unsafe_allow_html=True)