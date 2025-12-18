# Lovable2 🤖

An AI-powered engineering planning agent built with LangGraph and LangChain that converts user prompts into structured engineering plans and implementation tasks.

## Overview

Lovable2 is an intelligent agent system that helps transform high-level project ideas into detailed engineering plans. Using advanced language models via Groq, it analyzes user requirements and generates comprehensive project structures with file specifications and implementation tasks.

## Features

- 🎯 **Planner Agent**: Converts user prompts into complete engineering plans
- 🏗️ **Architect Agent**: Breaks down plans into explicit, dependency-ordered tasks
- 📋 **Structured Outputs**: Uses Pydantic models for type-safe plan generation
- 🔄 **Graph-based Workflow**: Built on LangGraph for flexible agent orchestration
- ⚡ **Groq Integration**: Leverages fast LLM inference for quick planning

## Project Structure

```
Lovable2/
├── agent/
│   ├── graph.py         # Main agent graph and workflow logic
│   ├── prompts.py       # Prompt templates for planner and architect
│   └── states.py        # Pydantic models for structured outputs
├── main.py              # Entry point (placeholder)
├── pyproject.toml       # Project dependencies and metadata
└── README.md            # This file
```

## Installation

### Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Lovable2
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```
   
   Or using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   Create a `.env` file in the project root:
   ```bash
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Usage

### Basic Example

```python
from agent.graph import agent

# Define your project idea
user_prompt = "create a simple calculator web application"

# Generate a plan
result = agent.invoke({"user_prompt": user_prompt})

# Access the generated plan
plan = result["plan"]
print(f"Project: {plan.name}")
print(f"Tech Stack: {plan.techstack}")
print(f"Features: {plan.features}")
print(f"Files to create: {[f.path for f in plan.files]}")
```

### Output Structure

The planner agent generates a structured `Plan` object containing:

- **name**: Project name
- **description**: Brief project description
- **techstack**: Recommended technology stack
- **features**: List of key features to implement
- **files**: List of files with their paths and purposes

## Data Models

### Plan
Represents the overall project structure:
- `name`: Application name
- `description`: One-line app description
- `techstack`: Technologies to be used
- `features`: List of features
- `files`: List of File objects

### File
Describes a single file in the project:
- `path`: File location
- `purpose`: Explanation of the file's role

### ImplementationTask
Represents a specific implementation task:
- `filepath`: Target file path
- `task_description`: Detailed task instructions

### TaskPlan
Collection of implementation tasks:
- `implementation_task`: List of ImplementationTask objects

## Dependencies

- **langchain** (≥0.3.27): Framework for LLM applications
- **langgraph** (≥0.6.3): Graph-based agent orchestration
- **groq** (≥0.31.0): Fast LLM inference API
- **pydantic** (≥2.11.7): Data validation and settings management
- **python-dotenv** (≥1.1.1): Environment variable management

## Configuration

### Environment Variables

- `GROQ_API_KEY`: Your Groq API key (required)

### Model Configuration

The default model is `openai/gpt-oss-120b`. To change it, modify the LLM initialization in `agent/graph.py`:

```python
llm = ChatGroq(model="your-preferred-model")
```

## Development

### Running the Agent

Execute the main graph script:

```bash
python agent/graph.py
```

### Extending the Agent

To add new agent nodes:

1. Define your agent function in `agent/graph.py`
2. Add the node to the StateGraph
3. Connect it to the workflow using `add_edge`

Example:
```python
def new_agent(state: dict) -> dict:
    # Your agent logic
    return {"key": value}

graph.add_node("new_agent", new_agent)
graph.add_edge("planner", "new_agent")
```

## Roadmap

- [ ] Implement full architect agent integration
- [ ] Add code generation capabilities
- [ ] Support for multiple LLM providers
- [ ] Interactive CLI interface
- [ ] Web UI for plan visualization
- [ ] Export plans to various formats (JSON, Markdown, etc.)

## License

[Add your license here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

Built with:
- [LangChain](https://github.com/langchain-ai/langchain)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Groq](https://groq.com/)

