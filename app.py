import streamlit as st
from agentforge.workflow import run_manager_agent

st.set_page_config(
    page_title="AgentForge",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AgentForge")
st.subheader("Multi-Agent Software Team Builder")

project_idea = st.text_area(
    "Describe the software you want to build",
    placeholder="Example: Build a task manager API with authentication...",
    height=160,
    width=900
)

if st.button("Run Manager Agent"):
    if not project_idea.strip():
        st.error("Please enter a project idea.")
    else:
        try:
            with st.spinner("Manager Agent is planning your project..."):
                blueprint = run_manager_agent(project_idea)

            st.success("Manager Agent completed the project blueprint.")

            st.header("📋 Project Summary")
            st.write(f"**Project Name:** {blueprint.project_name}")
            st.write(f"**Project Type:** {blueprint.project_type}")
            st.write(f"**Complexity:** {blueprint.complexity}")
            st.write(f"**Estimated Timeline:** {blueprint.estimated_timeline}")
            st.write(blueprint.description)

            st.header("🧰 Recommended Stack")
            st.write(f"**Frontend:** {blueprint.recommended_stack.frontend}")
            st.write(f"**Backend:** {blueprint.recommended_stack.backend}")
            st.write(f"**Database:** {blueprint.recommended_stack.database}")
            st.write(f"**Deployment:** {blueprint.recommended_stack.deployment}")

            st.header("📦 Modules")
            for module in blueprint.modules:
                st.write(f"- {module}")

            st.header("✨ Features")
            for feature in blueprint.features:
                st.write(f"- {feature}")

            st.header("🗄️ Database Design")
            st.subheader("Entities")
            for entity in blueprint.database_entities:
                st.write(f"- {entity}")

            st.subheader("Relationships")
            for relationship in blueprint.relationships:
                st.write(f"- {relationship}")

            st.header("👥 Agent Assignments")

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

            st.header("🗂️ Folder Structure")
            st.code("\n".join(blueprint.folder_structure))

            st.header("⚠️ Risks")
            for risk in blueprint.risks:
                st.write(f"- {risk}")

            st.header("➡️ Next Action")
            st.success(f"{blueprint.next_agent} should begin.")

        except Exception as e:
            st.error("The model is temporarily unavailable or rate-limited. Please try again in a few minutes.")
            st.code(str(e))