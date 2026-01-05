

from agent.prompts import *
from agent.states import *
from agent.tools import *
from langchain_core.globals import set_verbose, set_debug
from langgraph.constants import END
from langgraph.graph import StateGraph
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
_ = load_dotenv()

# set_debug(True)
# set_verbose(True)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def planner_agent(state:dict) -> dict:
    users_prompt: str = state["user_prompt"]
    resp = llm.with_structured_output(Plan, method="function_calling").invoke(planner_prompt(users_prompt))
    if resp is None:
        raise ValueError("Planner did not return a valid response")
    return {"plan": resp }

def architect_agent(state: dict) -> dict:
    plan: Plan = state ["plan"]
    resp = llm.with_structured_output(TaskPlan, method="function_calling").invoke(architect_prompt(plan))
    if resp is None:
        raise ValueError("Architect did not return a valid response")
    resp.plan = plan
    return {"task_plan": resp }


def coder_agent(state: dict) -> dict:
    coder_state = state.get("coder_state")

    if coder_state is None:
        coder_state = CoderState(task_plan=state["task_plan"], current_step_idx=0)

    steps = coder_state.task_plan.implementation_task

    if coder_state.current_step_idx >= len(steps):
        return {"coder_state": coder_state, "status": "DONE"}

    current_task = steps[coder_state.current_step_idx]

    existing_content = read_file.run(current_task.filepath)

    user_prompt = (
        f"Task: {current_task.task_description} \n"
        f"File: {current_task.filepath} \n"
        f"Existing content: \n{existing_content}\n"
        "Use write_file (path, content) to save your changes."
    )

    system_prompt = coder_system_prompt()
    resp = llm.invoke(system_prompt + user_prompt)

    coder_tools = [read_file, write_file, list_files, get_current_directory]

    llm_with_tools = llm.bind_tools(coder_tools)

    react_agent = create_agent(llm_with_tools, coder_tools)
    react_agent.invoke({
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    })

    coder_state.current_step_idx += 1

    return {"coder_state": coder_state}

graph = StateGraph(dict)
graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)

graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")
graph.add_conditional_edges(
    "coder",
    lambda s: "END" if s.get("status") == "DONE" else "coder",
    {"END":END, "coder": "coder"}
)

graph.set_entry_point("planner")

agent = graph.compile()

if __name__ == "__main__":
    user_prompt = "create a simple calculator web application"

    result = agent.invoke({"user_prompt": user_prompt},
                          {"recursion_limit": 100})
    print(result)

