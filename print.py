import streamlit as st

def display_json_data(data, prefix=""):
    for key, value in data.items():
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    display_json_data(item, f"{prefix}{key.capitalize()}: ")
                else:
                    st.write(f"{prefix}{item}")
        elif isinstance(value, dict):
            display_json_data(value, f"{prefix}{key.capitalize()}: ")
        else:
            st.write(f"{prefix}{key.capitalize()}: {value}")

# Your JSON-like response from the GPT model
itinerary_json = {
    "day1": [
        {
            "title": "Activity 1",
            "description": "Description of Activity 1",
            "link": "https://example.com/activity1",
            "time": "9:00"
        },
        {
            "title": "Activity 2",
            "description": "Description of Activity 2",
            "link": "https://example.com/activity2",
        },
    ],
    "day2": [
        {
            "title": "Another Activity 1",
            "description": "Description of Another Activity 1",
            "link": "https://example.com/another_activity1",
        },
        {
            "title": "Another Activity 2",
            "description": "Description of Another Activity 2",
            "link": "https://example.com/another_activity2",
        },
    ],
}

# Streamlit app title
st.title("Display JSON Data")

# Display the JSON-like response
display_json_data(itinerary_json)
