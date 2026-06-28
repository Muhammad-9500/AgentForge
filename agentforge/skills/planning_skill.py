def create_project_breakdown(project_idea: str) -> str:
    """
    Breaks a software idea into major modules.
    This is our first reusable AgentForge skill.
    """
    return f"""
Project Idea:
{project_idea}

Suggested Modules:
1. Authentication
2. Core Business Features
3. Database Layer
4. API Layer
5. Frontend Interface
6. Testing
7. Deployment
"""