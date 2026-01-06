# 🚀 Lovable2 Streamlit UI Guide

## Quick Start

### Option 1: Using the Run Script
```bash
./run_streamlit.sh
```

### Option 2: Manual Start
```bash
source .venv/bin/activate
streamlit run app.py
```

## Features

### 🎯 Modern Web Interface
- **Beautiful UI** - Clean, gradient-based design with modern styling
- **Real-time Progress** - Watch your project being generated step-by-step
- **Interactive Results** - Explore the plan, tasks, and implementation in organized tabs

### 📋 Key Components

1. **Project Input**
   - Enter your project idea in natural language
   - Use quick example prompts to get started
   - Adjustable recursion limit for complex projects

2. **Generation Process**
   - Visual progress bar
   - Status updates for each agent (Planner → Architect → Coder)
   - Error handling with detailed traceback

3. **Results Display**
   - **Project Plan Tab**: View the high-level project structure, tech stack, and features
   - **Task Breakdown Tab**: See all implementation tasks broken down by file
   - **Implementation Tab**: Track completion status
   - **Raw Output Tab**: Inspect the full JSON response

### ⚙️ Configuration

- **Recursion Limit**: Adjust the slider in the sidebar (10-200)
  - Lower values for simple projects
  - Higher values for complex multi-file projects

### 🎨 Example Prompts

Try these to get started:
- "A simple calculator web app"
- "A to-do list with dark mode"
- "A blog website with comments"
- "A weather dashboard app"

## Tips

1. **Clear Results**: Use the sidebar button to clear previous results
2. **Error Debugging**: Check the "View Error Details" expander if something goes wrong
3. **Generated Files**: Look in the `generated_project` directory for actual code
4. **Status Tracking**: Watch the progress bar and status messages during generation

## Troubleshooting

### Port Already in Use
If port 8501 is already in use:
```bash
streamlit run app.py --server.port 8502
```

### Environment Variables
Make sure your `.env` file contains:
```
OPENAI_API_KEY=your_api_key_here
```

### Module Not Found Errors
Reinstall dependencies:
```bash
uv pip install -e .
```

## Architecture

The Streamlit UI integrates with the LangGraph agent system:

```
User Input → Planner Agent → Architect Agent → Coder Agent → Results Display
```

Each agent's output is captured and displayed in a structured, user-friendly format.

---

Made with ❤️ using LangGraph, OpenAI, and Streamlit

