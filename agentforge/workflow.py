import asyncio
import json
import uuid

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agentforge.agents.manager_agent import manager_agent
from agentforge.agents.backend_agent import backend_agent
from agentforge.agents.frontend_agent import frontend_agent
from agentforge.agents.testing_agent import testing_agent
from agentforge.agents.devops_agent import devops_agent
from agentforge.agents.documentation_agent import documentation_agent
from agentforge.agents.reviewer_agent import reviewer_agent

from agentforge.guardrails import Guardrails
from agentforge.models import ProjectBlueprint, BackendPlan, FrontendPlan, TestingPlan, DevOpsPlan, DocumentationPlan, ReviewerPlan

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
    clean_project_idea = project_idea.strip()
    validation = Guardrails().validate(clean_project_idea)
    if not validation.valid:
        raise ValueError(f"Guardrails validation failed: {validation.message}")

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


async def run_backend_agent_async(blueprint: ProjectBlueprint) -> BackendPlan:
    session_service = InMemorySessionService()

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=str(uuid.uuid4()),
    )

    runner = Runner(
        app_name=APP_NAME,
        agent=backend_agent,
        session_service=session_service,
    )

    blueprint_json = blueprint.model_dump_json(indent=2)

    message = types.Content(
        role="user",
        parts=[
            types.Part(
                text=f"""
Create a backend technical implementation plan from this project blueprint:

{blueprint_json}
"""
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
        raise ValueError("Backend Agent returned an empty response.")

    try:
        cleaned_response = clean_json_response(final_response)
        backend_data = json.loads(cleaned_response)
        backend_plan = BackendPlan(**backend_data)
        return backend_plan

    except Exception as e:
        raise ValueError(
            f"Failed to parse Backend Agent response as BackendPlan: {e}\n\n"
            f"Raw response:\n{final_response}"
        )

async def run_frontend_agent_async(
    blueprint: ProjectBlueprint,
    backend_plan: BackendPlan
) -> FrontendPlan:
    session_service = InMemorySessionService()

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=str(uuid.uuid4()),
    )

    runner = Runner(
        app_name=APP_NAME,
        agent=frontend_agent,
        session_service=session_service,
    )

    blueprint_json = blueprint.model_dump_json(indent=2)
    backend_json = backend_plan.model_dump_json(indent=2)

    message = types.Content(
        role="user",
        parts=[
            types.Part(
                text=f"""
Create a frontend technical implementation plan using this project blueprint and backend plan.

PROJECT BLUEPRINT:
{blueprint_json}

BACKEND PLAN:
{backend_json}
"""
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
        raise ValueError("Frontend Agent returned an empty response.")

    try:
        cleaned_response = clean_json_response(final_response)
        frontend_data = json.loads(cleaned_response)
        frontend_plan = FrontendPlan(**frontend_data)
        return frontend_plan

    except Exception as e:
        raise ValueError(
            f"Failed to parse Frontend Agent response as FrontendPlan: {e}\n\n"
            f"Raw response:\n{final_response}"
        )

async def run_testing_agent_async(
    blueprint: ProjectBlueprint,
    backend_plan: BackendPlan,
    frontend_plan: FrontendPlan
) -> TestingPlan:
    session_service = InMemorySessionService()

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=str(uuid.uuid4()),
    )

    runner = Runner(
        app_name=APP_NAME,
        agent=testing_agent,
        session_service=session_service,
    )

    message = types.Content(
        role="user",
        parts=[
            types.Part(
                text=f"""
Create a complete testing strategy from this project information.

PROJECT BLUEPRINT:
{blueprint.model_dump_json(indent=2)}

BACKEND PLAN:
{backend_plan.model_dump_json(indent=2)}

FRONTEND PLAN:
{frontend_plan.model_dump_json(indent=2)}
"""
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
        raise ValueError("Testing Agent returned an empty response.")

    try:
        cleaned_response = clean_json_response(final_response)
        testing_data = json.loads(cleaned_response)
        testing_plan = TestingPlan(**testing_data)
        return testing_plan

    except Exception as e:
        raise ValueError(
            f"Failed to parse Testing Agent response as TestingPlan: {e}\n\n"
            f"Raw response:\n{final_response}"
        )

async def run_devops_agent_async(
    blueprint: ProjectBlueprint,
    backend_plan: BackendPlan,
    frontend_plan: FrontendPlan,
    testing_plan: TestingPlan
) -> DevOpsPlan:
    session_service = InMemorySessionService()

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=str(uuid.uuid4()),
    )

    runner = Runner(
        app_name=APP_NAME,
        agent=devops_agent,
        session_service=session_service,
    )

    message = types.Content(
        role="user",
        parts=[
            types.Part(
                text=f"""
Create a complete DevOps and deployment strategy from this project information.

PROJECT BLUEPRINT:
{blueprint.model_dump_json(indent=2)}

BACKEND PLAN:
{backend_plan.model_dump_json(indent=2)}

FRONTEND PLAN:
{frontend_plan.model_dump_json(indent=2)}

TESTING PLAN:
{testing_plan.model_dump_json(indent=2)}
"""
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
        raise ValueError("DevOps Agent returned an empty response.")

    try:
        cleaned_response = clean_json_response(final_response)
        devops_data = json.loads(cleaned_response)
        devops_plan = DevOpsPlan(**devops_data)
        return devops_plan

    except Exception as e:
        raise ValueError(
            f"Failed to parse DevOps Agent response as DevOpsPlan: {e}\n\n"
            f"Raw response:\n{final_response}"
        )

async def run_documentation_agent_async(
    blueprint: ProjectBlueprint,
    backend_plan: BackendPlan,
    frontend_plan: FrontendPlan,
    testing_plan: TestingPlan,
    devops_plan: DevOpsPlan
) -> DocumentationPlan:
    session_service = InMemorySessionService()

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=str(uuid.uuid4()),
    )

    runner = Runner(
        app_name=APP_NAME,
        agent=documentation_agent,
        session_service=session_service,
    )

    message = types.Content(
        role="user",
        parts=[
            types.Part(
                text=f"""
Create complete starter documentation from this project information.

PROJECT BLUEPRINT:
{blueprint.model_dump_json(indent=2)}

BACKEND PLAN:
{backend_plan.model_dump_json(indent=2)}

FRONTEND PLAN:
{frontend_plan.model_dump_json(indent=2)}

TESTING PLAN:
{testing_plan.model_dump_json(indent=2)}

DEVOPS PLAN:
{devops_plan.model_dump_json(indent=2)}
"""
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
        raise ValueError("Documentation Agent returned an empty response.")

    try:
        cleaned_response = clean_json_response(final_response)
        documentation_data = json.loads(cleaned_response)
        documentation_plan = DocumentationPlan(**documentation_data)
        return documentation_plan

    except Exception as e:
        raise ValueError(
            f"Failed to parse Documentation Agent response as DocumentationPlan: {e}\n\n"
            f"Raw response:\n{final_response}"
        )

async def run_reviewer_agent_async(
    blueprint: ProjectBlueprint,
    backend_plan: BackendPlan,
    frontend_plan: FrontendPlan,
    testing_plan: TestingPlan,
    devops_plan: DevOpsPlan,
    documentation_plan: DocumentationPlan
) -> ReviewerPlan:
    session_service = InMemorySessionService()

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=str(uuid.uuid4()),
    )

    runner = Runner(
        app_name=APP_NAME,
        agent=reviewer_agent,
        session_service=session_service,
    )

    message = types.Content(
        role="user",
        parts=[
            types.Part(
                text=f"""
Perform a senior staff engineer design review of this generated project plan.

PROJECT BLUEPRINT:
{blueprint.model_dump_json(indent=2)}

BACKEND PLAN:
{backend_plan.model_dump_json(indent=2)}

FRONTEND PLAN:
{frontend_plan.model_dump_json(indent=2)}

TESTING PLAN:
{testing_plan.model_dump_json(indent=2)}

DEVOPS PLAN:
{devops_plan.model_dump_json(indent=2)}

DOCUMENTATION PLAN:
{documentation_plan.model_dump_json(indent=2)}
"""
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
        raise ValueError("Reviewer Agent returned an empty response.")

    try:
        cleaned_response = clean_json_response(final_response)
        reviewer_data = json.loads(cleaned_response)
        reviewer_plan = ReviewerPlan(**reviewer_data)
        return reviewer_plan

    except Exception as e:
        raise ValueError(
            f"Failed to parse Reviewer Agent response as ReviewerPlan: {e}\n\n"
            f"Raw response:\n{final_response}"
        )

def run_with_retry(async_func, *args):
    import time

    last_error = None

    for _ in range(3):
        try:
            return asyncio.run(async_func(*args))
        except Exception as e:
            last_error = e
            time.sleep(3)

    raise last_error

def run_manager_agent(project_idea: str) -> ProjectBlueprint:
    return run_with_retry(run_manager_agent_async, project_idea)


def run_backend_agent(blueprint: ProjectBlueprint) -> BackendPlan:
    return run_with_retry(run_backend_agent_async, blueprint)

def run_frontend_agent(
    blueprint: ProjectBlueprint,
    backend_plan: BackendPlan
) -> FrontendPlan:
    return run_with_retry(run_frontend_agent_async, blueprint, backend_plan)

def run_testing_agent(
    blueprint: ProjectBlueprint,
    backend_plan: BackendPlan,
    frontend_plan: FrontendPlan
) -> TestingPlan:
    return run_with_retry(
        run_testing_agent_async,
        blueprint,
        backend_plan,
        frontend_plan
    )

def run_devops_agent(
    blueprint: ProjectBlueprint,
    backend_plan: BackendPlan,
    frontend_plan: FrontendPlan,
    testing_plan: TestingPlan
) -> DevOpsPlan:
    return run_with_retry(
        run_devops_agent_async,
        blueprint,
        backend_plan,
        frontend_plan,
        testing_plan
    )

def run_documentation_agent(
    blueprint: ProjectBlueprint,
    backend_plan: BackendPlan,
    frontend_plan: FrontendPlan,
    testing_plan: TestingPlan,
    devops_plan: DevOpsPlan
) -> DocumentationPlan:
    return run_with_retry(
        run_documentation_agent_async,
        blueprint,
        backend_plan,
        frontend_plan,
        testing_plan,
        devops_plan
    )

def run_reviewer_agent(
    blueprint: ProjectBlueprint,
    backend_plan: BackendPlan,
    frontend_plan: FrontendPlan,
    testing_plan: TestingPlan,
    devops_plan: DevOpsPlan,
    documentation_plan: DocumentationPlan
) -> ReviewerPlan:
    return run_with_retry(
        run_reviewer_agent_async,
        blueprint,
        backend_plan,
        frontend_plan,
        testing_plan,
        devops_plan,
        documentation_plan
    )
