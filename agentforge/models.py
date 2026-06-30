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

class BackendPlan(BaseModel):
    framework: str
    architecture: List[str]
    services: List[str]
    api_endpoints: List[str]
    database_plan: List[str]
    authentication_plan: List[str]
    validation_plan: List[str]
    files_to_create: List[str]
    risks: List[str]
    next_agent: str

class FrontendPlan(BaseModel):
    framework: str
    ui_architecture: List[str]
    pages: List[str]
    components: List[str]
    state_management: List[str]
    api_integration: List[str]
    styling_plan: List[str]
    files_to_create: List[str]
    risks: List[str]
    next_agent: str

class TestingPlan(BaseModel):
    testing_framework: str
    unit_tests: List[str]
    integration_tests: List[str]
    end_to_end_tests: List[str]
    api_tests: List[str]
    frontend_tests: List[str]
    security_tests: List[str]
    performance_tests: List[str]
    files_to_create: List[str]
    risks: List[str]
    next_agent: str

class DevOpsPlan(BaseModel):
    dockerfile_plan: List[str]
    docker_compose_plan: List[str]
    environment_variables: List[str]
    ci_cd_workflow: List[str]
    deployment_instructions: List[str]
    monitoring_logging_notes: List[str]
    files_to_create: List[str]
    risks: List[str]
    next_agent: str

class DocumentationPlan(BaseModel):
    readme: str
    project_overview: str
    architecture: str
    tech_stack: List[str]
    folder_structure: List[str]
    installation: List[str]
    running_the_project: List[str]
    api_overview: List[str]
    testing_instructions: List[str]
    deployment_instructions: List[str]
    future_improvements: List[str]
    contributing: str
    changelog: str
    license: str
    files_to_create: List[str]
    risks: List[str]
    next_agent: str

class ReviewerPlan(BaseModel):
    overall_score: str
    architecture_consistency: List[str]
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    security_issues: List[str]
    api_review: List[str]
    frontend_backend_alignment: List[str]
    testing_gaps: List[str]
    deployment_concerns: List[str]
    documentation_gaps: List[str]
    scalability_notes: List[str]
    database_review: List[str]
    next_step: str
