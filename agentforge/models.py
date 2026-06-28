from pydantic import BaseModel
from typing import List


class TechnologyStack(BaseModel):
    frontend: str
    backend: str
    database: str
    deployment: str


class AgentAssignments(BaseModel):
    backend_agent: List[str]
    frontend_agent: List[str]
    testing_agent: List[str]
    devops_agent: List[str]
    documentation_agent: List[str]
    reviewer_agent: List[str]


class ProjectBlueprint(BaseModel):
    project_name: str
    project_type: str
    description: str
    complexity: str
    estimated_timeline: str
    recommended_stack: TechnologyStack
    modules: List[str]
    features: List[str]
    database_entities: List[str]
    relationships: List[str]
    agent_assignments: AgentAssignments
    folder_structure: List[str]
    risks: List[str]
    next_agent: str