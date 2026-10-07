# Personal Travel Planner Agent

## Overview

Personal Travel Planner is an AI travel planning agent built using Google ADK (Agent Development Kit).

The agent takes a user's travel requirements and creates a simple, practical and budget-friendly itinerary.

## Features

- Understands destination and trip duration
- Considers user's budget
- Understands interests and food preferences
- Recommends suitable places to visit
- Creates a day-wise itinerary
- Provides a budget estimate
- Includes accommodation, food, transportation and activity costs
- Provides local food recommendations
- Gives practical travel tips
- Checks whether the estimated cost is within the user's budget

## Security & Guardrails

The agent includes basic security guardrails to keep the assistant focused on its intended purpose.

### Role Restriction
- The agent is restricted to travel planning and closely related travel topics.
- Unrelated requests are politely redirected to travel-related assistance.

### Prompt Injection Protection
- The agent does not follow requests to ignore or override its instructions.
- It does not reveal system or hidden instructions.
- User-provided content is treated as data rather than instructions that can change the agent's role.

### Secret Protection
The agent is instructed not to reveal:
- API keys
- Passwords
- Access tokens
- Credentials
- Environment variables
- `.env` file contents
- Private configuration

### Safety Protection
- Requests involving hacking, security bypassing, malware, phishing or password cracking are rejected.
- The agent remains focused on safe travel assistance.

### Input Guardrail
A `before_model_callback` is used to detect clearly unrelated or unsafe requests before the model processes them.

## Guardrail Testing

The following security tests were performed:

| Test | Result |
|---|---|
| Normal travel planning request | PASS |
| Prompt injection attempt | PASS |
| API key / `.env` extraction attempt | PASS |
| Security bypass request | PASS |
| Unrelated Python/banking request | PASS |

The agent successfully redirected blocked requests instead of generating unrelated or unsafe content.

## Technologies Used

- Python
- Google ADK
- Gemini model
- VS Code

## Project Structure

```text
personal_travel_planner/
│
├── personal_travel_planner/
│   ├── __init__.py
│   └── agent.py
│
├── .env
├── requirements.txt
├── README.md
└── agent.py