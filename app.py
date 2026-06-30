import streamlit as st
from agentforge.workflow import (
    run_manager_agent,
    run_backend_agent,
    run_frontend_agent,
    run_testing_agent,
    run_devops_agent,
    run_documentation_agent,
    run_reviewer_agent
)

st.set_page_config(
    page_title="AgentForge",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AgentForge")
st.subheader("Multi-Agent Software Team Builder")

# -----------------------------
# Session State
# -----------------------------
if "blueprint" not in st.session_state:
    st.session_state.blueprint = None

if "backend_plan" not in st.session_state:
    st.session_state.backend_plan = None

if "frontend_plan" not in st.session_state:
    st.session_state.frontend_plan = None

if "testing_plan" not in st.session_state:
    st.session_state.testing_plan = None

if "devops_plan" not in st.session_state:
    st.session_state.devops_plan = None

if "documentation_plan" not in st.session_state:
    st.session_state.documentation_plan = None

if "reviewer_plan" not in st.session_state:
    st.session_state.reviewer_plan = None

# -----------------------------
# Project Input
# ----------------
project_idea = st.text_area(
    "Describe the software you want to build",
    placeholder="Example: Build a sophisticated high-end precision scientific calculator...",
    height=140,
)

if st.button("🚀 Generate Project Blueprint"):
    if not project_idea.strip():
        st.error("Please enter a project idea.")
    else:
        try:
            with st.spinner("Manager Agent is creating the project blueprint..."):
                st.session_state.blueprint = run_manager_agent(project_idea)

                # Reset downstream agents when a new project is generated
                st.session_state.backend_plan = None
                st.session_state.frontend_plan = None
                st.session_state.testing_plan = None
                st.session_state.devops_plan = None
                st.session_state.documentation_plan = None
                st.session_state.reviewer_plan = None

            st.success("Manager Agent completed the project blueprint.")
            st.rerun()

        except Exception as e:
            st.error("The model is temporarily unavailable or rate-limited. Please try again.")
            st.code(str(e))


blueprint = st.session_state.blueprint
backend_plan = st.session_state.backend_plan
frontend_plan = st.session_state.frontend_plan
testing_plan = st.session_state.testing_plan
devops_plan = st.session_state.devops_plan
documentation_plan = st.session_state.documentation_plan
reviewer_plan = st.session_state.reviewer_plan


# -----------------------------
# Workflow Dashboard
# -----------------------------
if blueprint:
    st.divider()
    st.header("✅ Agent Workflow")

    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    with col1:
        st.success("Manager\n\nCompleted")

    with col2:
        if backend_plan:
            st.success("Backend\n\nCompleted")
        else:
            st.warning("Backend\n\nReady")

    with col3:
        if frontend_plan:
            st.success("Frontend\n\nCompleted")
        elif backend_plan:
            st.warning("Frontend\n\nReady")
        else:
            st.info("Frontend\n\nWaiting")

    with col4:
        if testing_plan:
            st.success("Testing\n\nCompleted")
        elif frontend_plan:
            st.warning("Testing\n\nReady")
        else:
            st.info("Testing\n\nWaiting")

    with col5:
        if devops_plan:
            st.success("DevOps\n\nCompleted")
        elif testing_plan:
            st.warning("DevOps\n\nReady")
        else:
            st.info("DevOps\n\nWaiting")

    with col6:
        if documentation_plan:
            st.success("Docs\n\nCompleted")
        elif devops_plan:
            st.warning("Docs\n\nReady")
        else:
            st.info("Docs\n\nWaiting")

    with col7:
        if reviewer_plan:
            st.success("Review\n\nCompleted")
        elif documentation_plan:
            st.warning("Review\n\nReady")
        else:
            st.info("Review\n\nWaiting")

    if not backend_plan:
        st.info("Next Recommended Agent: **backend_agent**")

        if st.button("🧠 Run Backend Agent"):
            try:
                with st.spinner("Backend Agent is designing the backend..."):
                    st.session_state.backend_plan = run_backend_agent(blueprint)

                st.success("Backend Agent completed the backend technical plan.")
                st.rerun()

            except Exception as e:
                st.error("Backend Agent failed. Please try again.")
                st.code(str(e))

    elif backend_plan and not frontend_plan:
        st.info("Next Recommended Agent: **frontend_agent**")

        if st.button("🎨 Run Frontend Agent"):
            try:
                with st.spinner("Frontend Agent is designing the frontend..."):
                    st.session_state.frontend_plan = run_frontend_agent(
                        blueprint,
                        backend_plan,
                    )

                st.success("Frontend Agent completed the frontend technical plan.")
                st.rerun()

            except Exception as e:
                st.error("Frontend Agent failed. Please try again.")
                st.code(str(e))

    elif frontend_plan and not testing_plan:
        st.info("Next Recommended Agent: **testing_agent**")

        if st.button(" Run Testing Agent"):
            try:
                with st.spinner("Testing Agent is creating the testing strategy..."):
                    st.session_state.testing_plan = run_testing_agent(
                        blueprint,
                        backend_plan,
                        frontend_plan,
                    )

                st.success("Testing Agent completed the testing strategy.")
                st.rerun()

            except Exception as e:
                st.error("Testing Agent failed. Please try again.")
                st.code(str(e))

    elif testing_plan and not devops_plan:
        st.info("Next Recommended Agent: **devops_agent**")

        if st.button(" Run DevOps Agent"):
            try:
                with st.spinner("DevOps Agent is creating the deployment strategy..."):
                    st.session_state.devops_plan = run_devops_agent(
                        blueprint,
                        backend_plan,
                        frontend_plan,
                        testing_plan,
                    )

                st.success("DevOps Agent completed the deployment strategy.")
                st.rerun()

            except Exception as e:
                st.error("DevOps Agent failed. Please try again.")
                st.code(str(e))

    elif devops_plan and not documentation_plan:
        st.info("Next Recommended Agent: **documentation_agent**")

        if st.button(" Run Documentation Agent"):
            try:
                with st.spinner("Documentation Agent is creating starter documentation..."):
                    st.session_state.documentation_plan = run_documentation_agent(
                        blueprint,
                        backend_plan,
                        frontend_plan,
                        testing_plan,
                        devops_plan,
                    )

                st.success("Documentation Agent completed the starter documentation.")
                st.rerun()

            except Exception as e:
                st.error("Documentation Agent failed. Please try again.")
                st.code(str(e))

    elif documentation_plan and not reviewer_plan:
        st.info("Next Recommended Agent: **reviewer_agent**")

        if st.button(" Run Reviewer Agent"):
            try:
                with st.spinner("Reviewer Agent is performing the design review..."):
                    st.session_state.reviewer_plan = run_reviewer_agent(
                        blueprint,
                        backend_plan,
                        frontend_plan,
                        testing_plan,
                        devops_plan,
                        documentation_plan,
                    )

                st.success("Reviewer Agent completed the design review.")
                st.rerun()

            except Exception as e:
                st.error("Reviewer Agent failed. Please try again.")
                st.code(str(e))

    elif reviewer_plan:
        st.success(f"Reviewer Agent completed. Next step: **{reviewer_plan.next_step}**")


# -----------------------------
# Project Snapshot
# -----------------------------
if blueprint:
    st.divider()
    st.header("📌 Project Snapshot")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Project", blueprint.project_name)

    with col2:
        st.metric("Type", blueprint.project_type)

    with col3:
        st.metric("Complexity", blueprint.complexity)

    with col4:
        st.metric("Timeline", blueprint.estimated_timeline)

    with st.expander("📋 Project Overview", expanded=False):
        st.write(blueprint.description)

    with st.expander("🧰 Recommended Stack", expanded=False):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.write("**Frontend**")
            st.info(blueprint.recommended_stack.frontend)

        with col2:
            st.write("**Backend**")
            st.info(blueprint.recommended_stack.backend)

        with col3:
            st.write("**Database**")
            st.info(blueprint.recommended_stack.database)

        with col4:
            st.write("**Deployment**")
            st.info(blueprint.recommended_stack.deployment)

    with st.expander("🏗 Technical Blueprint", expanded=False):
        st.subheader("Modules")
        for module in blueprint.modules:
            st.write(f"- {module}")

        st.subheader("Features")
        for feature in blueprint.features:
            st.write(f"- {feature}")

    with st.expander("🗄️ Database Design", expanded=False):
        st.subheader("Entities")
        for entity in blueprint.database_entities:
            st.write(f"- {entity}")

        st.subheader("Relationships")
        for relationship in blueprint.relationships:
            st.write(f"- {relationship}")

    with st.expander("📁 Folder Structure", expanded=False):
        st.code("\n".join(blueprint.folder_structure))

    with st.expander("⚠️ Risks", expanded=False):
        for risk in blueprint.risks:
            st.write(f"- {risk}")

    with st.expander("👥 Agent Assignments", expanded=False):
        st.subheader("Backend Agent")
        for task in blueprint.agent_assignments.backend_agent:
            st.write(f"✓ {task}")

        st.subheader("Frontend Agent")
        for task in blueprint.agent_assignments.frontend_agent:
            st.write(f"✓ {task}")

        st.subheader("Testing Agent")
        for task in blueprint.agent_assignments.testing_agent:
            st.write(f"✓ {task}")

        st.subheader("DevOps Agent")
        for task in blueprint.agent_assignments.devops_agent:
            st.write(f"✓ {task}")

        st.subheader("Documentation Agent")
        for task in blueprint.agent_assignments.documentation_agent:
            st.write(f"✓ {task}")

        st.subheader("Reviewer Agent")
        for task in blueprint.agent_assignments.reviewer_agent:
            st.write(f"✓ {task}")


# -----------------------------
# Backend Plan
# -----------------------------
if backend_plan:
    st.divider()
    st.header("🧠 Backend Technical Plan")

    st.write(f"**Framework:** {backend_plan.framework}")

    with st.expander("🏛 Backend Architecture", expanded=True):
        for item in backend_plan.architecture:
            st.write(f"- {item}")

    with st.expander("🧩 Services", expanded=False):
        for service in backend_plan.services:
            st.write(f"- {service}")

    with st.expander("🌐 API Endpoints", expanded=False):
        for endpoint in backend_plan.api_endpoints:
            st.write(f"- {endpoint}")

    with st.expander("🗄 Database Plan", expanded=False):
        for item in backend_plan.database_plan:
            st.write(f"- {item}")

    with st.expander("🔐 Authentication Plan", expanded=False):
        for item in backend_plan.authentication_plan:
            st.write(f"- {item}")

    with st.expander("✅ Validation Plan", expanded=False):
        for item in backend_plan.validation_plan:
            st.write(f"- {item}")

    with st.expander("📁 Files to Create", expanded=False):
        st.code("\n".join(backend_plan.files_to_create))

    with st.expander("⚠️ Backend Risks", expanded=False):
        for risk in backend_plan.risks:
            st.write(f"- {risk}")

    st.success(f"Next Agent: {backend_plan.next_agent}")


# -----------------------------
# Frontend Plan
# -----------------------------
if frontend_plan:
    st.divider()
    st.header("🎨 Frontend Technical Plan")

    st.write(f"**Framework:** {frontend_plan.framework}")

    with st.expander("🧱 UI Architecture", expanded=True):
        for item in frontend_plan.ui_architecture:
            st.write(f"- {item}")

    with st.expander("📄 Pages", expanded=False):
        for page in frontend_plan.pages:
            st.write(f"- {page}")

    with st.expander("🧩 Components", expanded=False):
        for component in frontend_plan.components:
            st.write(f"- {component}")

    with st.expander("🧠 State Management", expanded=False):
        for item in frontend_plan.state_management:
            st.write(f"- {item}")

    with st.expander("🌐 API Integration", expanded=False):
        for item in frontend_plan.api_integration:
            st.write(f"- {item}")

    with st.expander("🎨 Styling Plan", expanded=False):
        for item in frontend_plan.styling_plan:
            st.write(f"- {item}")

    with st.expander("📁 Files to Create", expanded=False):
        st.code("\n".join(frontend_plan.files_to_create))

    with st.expander("⚠️ Frontend Risks", expanded=False):
        for risk in frontend_plan.risks:
            st.write(f"- {risk}")

    st.success(f"Next Agent: {frontend_plan.next_agent}")


# -----------------------------
# Testing Plan
# -----------------------------
if testing_plan:
    st.divider()
    st.header(" Testing Strategy")

    st.write(f"**Testing Framework:** {testing_plan.testing_framework}")

    with st.expander(" Unit Tests", expanded=True):
        for item in testing_plan.unit_tests:
            st.write(f"- {item}")

    with st.expander(" Integration Tests", expanded=False):
        for item in testing_plan.integration_tests:
            st.write(f"- {item}")

    with st.expander(" End-to-End Tests", expanded=False):
        for item in testing_plan.end_to_end_tests:
            st.write(f"- {item}")

    with st.expander(" API Tests", expanded=False):
        for item in testing_plan.api_tests:
            st.write(f"- {item}")

    with st.expander(" Frontend Tests", expanded=False):
        for item in testing_plan.frontend_tests:
            st.write(f"- {item}")

    with st.expander(" Security Tests", expanded=False):
        for item in testing_plan.security_tests:
            st.write(f"- {item}")

    with st.expander(" Performance Tests", expanded=False):
        for item in testing_plan.performance_tests:
            st.write(f"- {item}")

    with st.expander(" Files to Create", expanded=False):
        st.code("\n".join(testing_plan.files_to_create))

    with st.expander(" Testing Risks", expanded=False):
        for risk in testing_plan.risks:
            st.write(f"- {risk}")

    st.success(f"Next Agent: {testing_plan.next_agent}")


# -----------------------------
# DevOps Plan
# -----------------------------
if devops_plan:
    st.divider()
    st.header(" DevOps Strategy")

    with st.expander(" Dockerfile Plan", expanded=True):
        for item in devops_plan.dockerfile_plan:
            st.write(f"- {item}")

    with st.expander(" Docker Compose Plan", expanded=False):
        for item in devops_plan.docker_compose_plan:
            st.write(f"- {item}")

    with st.expander(" Environment Variables", expanded=False):
        for item in devops_plan.environment_variables:
            st.write(f"- {item}")

    with st.expander(" CI/CD Workflow", expanded=False):
        for item in devops_plan.ci_cd_workflow:
            st.write(f"- {item}")

    with st.expander(" Deployment Instructions", expanded=False):
        for item in devops_plan.deployment_instructions:
            st.write(f"- {item}")

    with st.expander(" Monitoring and Logging Notes", expanded=False):
        for item in devops_plan.monitoring_logging_notes:
            st.write(f"- {item}")

    with st.expander(" Files to Create", expanded=False):
        st.code("\n".join(devops_plan.files_to_create))

    with st.expander(" DevOps Risks", expanded=False):
        for risk in devops_plan.risks:
            st.write(f"- {risk}")

    st.success(f"Next Agent: {devops_plan.next_agent}")


# -----------------------------
# Documentation Plan
# -----------------------------
if documentation_plan:
    st.divider()
    st.header(" Documentation")

    with st.expander(" README.md", expanded=True):
        st.code(documentation_plan.readme, language="markdown")

    with st.expander(" Project Overview", expanded=False):
        st.write(documentation_plan.project_overview)

    with st.expander(" Architecture", expanded=False):
        st.code(documentation_plan.architecture, language="markdown")

    with st.expander(" Tech Stack", expanded=False):
        for item in documentation_plan.tech_stack:
            st.write(f"- {item}")

    with st.expander(" Folder Structure", expanded=False):
        for item in documentation_plan.folder_structure:
            st.write(f"- {item}")

    with st.expander(" Installation", expanded=False):
        for item in documentation_plan.installation:
            st.write(f"- {item}")

    with st.expander(" Running the Project", expanded=False):
        for item in documentation_plan.running_the_project:
            st.write(f"- {item}")

    with st.expander(" API Overview", expanded=False):
        for item in documentation_plan.api_overview:
            st.write(f"- {item}")

    with st.expander(" Testing Instructions", expanded=False):
        for item in documentation_plan.testing_instructions:
            st.write(f"- {item}")

    with st.expander(" Deployment Instructions", expanded=False):
        for item in documentation_plan.deployment_instructions:
            st.write(f"- {item}")

    with st.expander(" Future Improvements", expanded=False):
        for item in documentation_plan.future_improvements:
            st.write(f"- {item}")

    with st.expander(" CONTRIBUTING.md", expanded=False):
        st.code(documentation_plan.contributing, language="markdown")

    with st.expander(" CHANGELOG.md", expanded=False):
        st.code(documentation_plan.changelog, language="markdown")

    with st.expander(" LICENSE", expanded=False):
        st.code(documentation_plan.license)

    with st.expander(" Files to Create", expanded=False):
        st.code("\n".join(documentation_plan.files_to_create))

    with st.expander(" Documentation Risks", expanded=False):
        for risk in documentation_plan.risks:
            st.write(f"- {risk}")

    st.success(f"Next Agent: {documentation_plan.next_agent}")


# -----------------------------
# Reviewer Plan
# -----------------------------
if reviewer_plan:
    st.divider()
    st.header(" Design Review")

    st.metric("Overall Score", reviewer_plan.overall_score)

    with st.expander(" Architecture Consistency", expanded=True):
        for item in reviewer_plan.architecture_consistency:
            st.write(f"- {item}")

    with st.expander(" Strengths", expanded=True):
        for item in reviewer_plan.strengths:
            st.write(f"- {item}")

    with st.expander(" Weaknesses", expanded=True):
        for item in reviewer_plan.weaknesses:
            st.write(f"- {item}")

    with st.expander(" Recommendations", expanded=True):
        for item in reviewer_plan.recommendations:
            st.write(f"- {item}")

    with st.expander(" Security Issues", expanded=False):
        for item in reviewer_plan.security_issues:
            st.write(f"- {item}")

    with st.expander(" API Review", expanded=False):
        for item in reviewer_plan.api_review:
            st.write(f"- {item}")

    with st.expander(" Frontend and Backend Alignment", expanded=False):
        for item in reviewer_plan.frontend_backend_alignment:
            st.write(f"- {item}")

    with st.expander(" Testing Gaps", expanded=False):
        for item in reviewer_plan.testing_gaps:
            st.write(f"- {item}")

    with st.expander(" Deployment Concerns", expanded=False):
        for item in reviewer_plan.deployment_concerns:
            st.write(f"- {item}")

    with st.expander(" Documentation Gaps", expanded=False):
        for item in reviewer_plan.documentation_gaps:
            st.write(f"- {item}")

    with st.expander(" Scalability Notes", expanded=False):
        for item in reviewer_plan.scalability_notes:
            st.write(f"- {item}")

    with st.expander(" Database Review", expanded=False):
        for item in reviewer_plan.database_review:
            st.write(f"- {item}")

    st.success(f"Next Step: {reviewer_plan.next_step}")
