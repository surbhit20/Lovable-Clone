import streamlit as st
import traceback
from agent.graph import agent
from agent.states import Plan, TaskPlan, ImplementationTask
import json

# Page config
st.set_page_config(
    page_title="UnLovable",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
    }
    .info-box {
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
    }
    .error-box {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
    }
    .step-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'result' not in st.session_state:
    st.session_state.result = None
if 'running' not in st.session_state:
    st.session_state.running = False
if 'error' not in st.session_state:
    st.session_state.error = None

# Header
st.markdown("""
<div class="main-header">
    <h1>🚀 UnLovable</h1>
    <p>Transform your ideas into complete project implementations</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    recursion_limit = st.slider("Recursion Limit", min_value=10, max_value=200, value=100, step=10)
    st.markdown("---")
    st.markdown("""
    ### How it works:
    1. **Planner** - Creates high-level project plan
    2. **Architect** - Breaks down into implementation tasks
    3. **Coder** - Implements each task step by step
    """)
    
    if st.button("🗑️ Clear Results"):
        st.session_state.result = None
        st.session_state.error = None
        st.rerun()

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📝 Enter Your Project Idea")
    user_prompt = st.text_area(
        "What would you like to build?",
        placeholder="e.g., A simple to-do list app with user authentication",
        height=100,
        disabled=st.session_state.running
    )

with col2:
    st.header("🎯 Quick Examples")
    example_prompts = [
        "A simple calculator web app",
        "A to-do list with dark mode",
        "A blog website with comments",
        "A weather dashboard app"
    ]
    for example in example_prompts:
        if st.button(f"💡 {example}", disabled=st.session_state.running, use_container_width=True):
            user_prompt = example
            st.rerun()

# Run button
if st.button("🚀 Generate Project", type="primary", disabled=st.session_state.running or not user_prompt):
    st.session_state.running = True
    st.session_state.result = None
    st.session_state.error = None
    
    # Progress placeholders
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.info("🤔 **Planner Agent** - Analyzing your requirements...")
        progress_bar.progress(20)
        
        # Run the agent
        result = agent.invoke(
            {"user_prompt": user_prompt},
            {"recursion_limit": recursion_limit}
        )
        
        progress_bar.progress(100)
        status_text.success("✅ Project generation complete!")
        
        st.session_state.result = result
        st.session_state.running = False
        st.rerun()
        
    except Exception as e:
        st.session_state.error = {
            "message": str(e),
            "traceback": traceback.format_exc()
        }
        st.session_state.running = False
        st.rerun()

# Display results
if st.session_state.error:
    st.error("❌ An error occurred during project generation")
    with st.expander("🔍 View Error Details"):
        st.code(st.session_state.error["message"])
        st.code(st.session_state.error["traceback"])

if st.session_state.result:
    st.markdown("---")
    st.header("📊 Generation Results")
    
    result = st.session_state.result
    
    # Debug: Show what keys are in the result
    if not result:
        st.warning("⚠️ Result is empty or None")
    else:
        st.info(f"✓ Result contains keys: {', '.join(result.keys())}")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Project Plan", "🏗️ Task Breakdown", "💻 Implementation", "📄 Raw Output"])
    
    with tab1:
        if "plan" in result and result["plan"] is not None:
            plan = result["plan"]
            
            st.markdown('<div class="step-card">', unsafe_allow_html=True)
            st.subheader(f"🎯 {plan.name}")
            st.write(plan.description)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🛠️ Tech Stack:**")
                st.info(plan.techstack)
            
            with col2:
                st.markdown("**✨ Features:**")
                for feature in plan.features:
                    st.write(f"• {feature}")
            
            st.markdown("**📁 Files to Create:**")
            for file in plan.files:
                with st.expander(f"📄 {file.path}"):
                    st.write(file.purpose)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ No plan data available")
            st.info("This might mean the planner agent didn't complete successfully. Check the Raw Output tab for details.")
    
    with tab2:
        if "task_plan" in result and result["task_plan"] is not None:
            task_plan = result["task_plan"]
            
            st.subheader(f"📝 Implementation Tasks ({len(task_plan.implementation_task)} steps)")
            
            for idx, task in enumerate(task_plan.implementation_task, 1):
                with st.expander(f"Step {idx}: {task.filepath}"):
                    st.markdown(f"**File:** `{task.filepath}`")
                    st.markdown("**Task:**")
                    st.write(task.task_description)
        else:
            st.warning("⚠️ No task plan data available")
            st.info("This might mean the architect agent didn't complete successfully. Check the Raw Output tab for details.")
    
    with tab3:
        if "coder_state" in result:
            coder_state = result["coder_state"]
            
            st.success(f"✅ Completed {coder_state.current_step_idx} implementation steps")
            
            if "status" in result and result["status"] == "DONE":
                st.balloons()
                st.success("🎉 All tasks completed successfully!")
            
            st.info("Check your `generated_project` directory for the implemented files.")
        else:
            st.warning("No implementation data available")
    
    with tab4:
        st.subheader("Raw State Output")
        st.write(f"**Keys in result:** {list(result.keys())}")
        st.json(result, expanded=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    Made with ❤️ using LangGraph and OpenAI • Powered by Streamlit
</div>
""", unsafe_allow_html=True)

