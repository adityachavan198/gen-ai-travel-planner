from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from ics import Calendar, Event
from datetime import datetime, timedelta
import json
import pickle
import google.generativeai as palm
import os

app = FastAPI()
palm.configure(api_key=os.getenv("PALM_API_KEY"))
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name
print(model)


def complete_prompt(prompt):
    prompt += ". Return the response in a properly formatted json string which can be imported in code using json.loads function in python."
    prompt += """Generate a structured JSON representation for the travel itinerary.

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
          "location": "Activity Location 1"
        },
        {
          "title": "Activity 2",
          "description": "Description of Activity 2",
          "link": "https://example.com/activity2",
          "start_time": "02:00 PM",
          "end_time": "04:00 PM",
          "location": "Activity Location 2"
        }
      ]
    },
    {
      "day": 2,
      "activities": [
        {
          "title": "Another Activity 1",
          "description": "Description of Another Activity 1",
          "link": "https://example.com/another_activity1",
          "start_time": "09:30 AM",
          "end_time": "11:30 AM",
          "location": "Another Activity Location 1"
        },
        {
          "title": "Another Activity 2",
          "description": "Description of Another Activity 2",
          "link": "https://example.com/another_activity2",
          "start_time": "01:00 PM",
          "end_time": "03:00 PM",
          "location": "Another Activity Location 2"
        }
      ]
    }
  ]
}

        Ensure that each day has a 'day' field and a list of 'activities' with 'title', 'description', 'start_time', 'end_time', and 'location' fields. Keep descriptions concise.
"""
    return prompt

# CORS (Cross-Origin Resource Sharing) Middleware for allowing requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this based on your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ItineraryRequest(BaseModel):
    city: str
    days: int
    art: bool
    museums: bool
    outdoor: bool
    indoor: bool
    kids_friendly: bool
    young_people: bool

@app.post("/generate_itinerary")
def generate_itinerary(request: ItineraryRequest):
    # Construct the PALM API request based on user input
    prompt = f"You are a travel expert. Give me an itinerary for {request.city}, for {request.days} days, I like to"
    if request.art:
        prompt += " explore art,"
    if request.museums:
        prompt += " visit museums,"
    if request.outdoor:
        prompt += " engage in outdoor activities,"
    if request.indoor:
        prompt += " explore indoor activities,"
    if request.kids_friendly:
        prompt += " find places suitable for kids,"
    if request.young_people:
        prompt += " discover places suitable for young people,"

    prompt = complete_prompt(prompt)
    completion = palm.generate_text(
    model=model,
    prompt=prompt,
    temperature=0,
    # The maximum length of the response
    max_output_tokens=1000,)
    itinerary = completion.result.strip()
    itinerary = itinerary[7:-3]
    print(type(itinerary))
    print(itinerary)

    # Convert the itinerary to JSON format for easier manipulation
    itinerary_json = json.loads(itinerary)

    return itinerary_json

@app.get("/export_to_calendar")
def export_to_calendar():
    # Logic for exporting the itinerary to a calendar file (ICS format)
    # ...

    return {"status": "success", "message": "Calendar file exported!"}
