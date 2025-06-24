from registry import AGENT_REGISTRY

def dispatch(request):
    agent_id = request["agent"]
    params = request.get("params", {})

    agent_cls = AGENT_REGISTRY.get(agent_id)
    if not agent_cls:
        raise ValueError(f"Neznámý agent: {agent_id}")

    agent = agent_cls()
    return agent.run(**params)