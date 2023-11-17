import streamlit as st
import pprint
import google.generativeai as palm
import os

palm.configure(api_key=os.getenv("PALM_API_KEY"))
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name
print(model)

# Streamlit app title and user input
st.title("Travel Itinerary Generator")

city = st.text_input("Enter the city you're visiting:")
days = st.number_input("Enter the number of days for your trip:", min_value=1, max_value=30)

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
    
    prompt = f"You are an travel expert. Give me an itenary for {city}, for {days} days, I like to"
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

    # Call the OpenAI API
    completion = palm.generate_text(
    model=model,
    prompt=prompt,
    temperature=0,
    # The maximum length of the response
    max_output_tokens=800,
)

    # Extract and display the generated itinerary
    itinerary = completion.result.strip()
    st.subheader("Your Personalized Itinerary:")
    st.write(itinerary)
