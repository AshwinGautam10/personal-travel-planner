import asyncio

from dotenv import load_dotenv
load_dotenv(r"C:\Users\ashwi\personal_travel_planner\.env")

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent import root_agent


async def main():
    session_service = InMemorySessionService()

    runner = Runner(
        agent=root_agent,
        app_name="travel_planner_eval",
        session_service=session_service,
    )

    session = await session_service.create_session(
        app_name="travel_planner_eval",
        user_id="eval_user",
    )

    content = types.Content(
        role="user",
        parts=[
            types.Part(
                text=(
                    "Plan a 3-day trip to Jaipur with a budget of "
                    "₹15,000. I like history and local food."
                )
            )
        ],
    )

    print("=" * 60)
    print("RUNNING TRAVEL PLANNER AGENT")
    print("=" * 60)

    async for event in runner.run_async(
        user_id="eval_user",
        session_id=session.id,
        new_message=content,
    ):
        if event.content:
            for part in event.content.parts:
                if part.text:
                    print(part.text)

    print("=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())