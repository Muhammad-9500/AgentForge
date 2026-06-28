import asyncio
import json
import uuid

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agentforge.agents.manager_agent import manager_agent
from agentforge.models import ProjectBlueprint

load_dotenv()

APP_NAME = "agentforge"
USER_ID = "demo_user"


def clean_json_response(response: str) -> str:
    response = response.strip()

    if response.startswith("```json"):
        response = response[7:].strip()

    if response.startswith("```"):
        response = response[3:].strip()

    if response.endswith("```"):
        response = response[:-3].strip()

    return response


async def run_manager_agent_async(project_idea: str) -> ProjectBlueprint:
    session_service = InMemorySessionService()

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=str(uuid.uuid4()),
    )

    runner = Runner(
        app_name=APP_NAME,
        agent=manager_agent,
        session_service=session_service,
    )

    clean_project_idea = project_idea.strip()

    message = types.Content(
        role="user",
        parts=[
            types.Part(
                text=f"Create a software project blueprint for this idea:\n\n{clean_project_idea}"
            )
        ],
    )

    final_response = ""

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text

    if not final_response:
        raise ValueError("Manager Agent returned an empty response.")

    try:
        cleaned_response = clean_json_response(final_response)
        blueprint_data = json.loads(cleaned_response)
        blueprint = ProjectBlueprint(**blueprint_data)
        return blueprint

    except Exception as e:
        raise ValueError(
            f"Failed to parse Manager Agent response as ProjectBlueprint: {e}\n\n"
            f"Raw response:\n{final_response}"
        )


def run_manager_agent(project_idea: str) -> ProjectBlueprint:
    import time

    last_error = None

    for attempt in range(3):
        try:
            return asyncio.run(run_manager_agent_async(project_idea))
        except Exception as e:
            last_error = e
            time.sleep(3)

    raise last_error