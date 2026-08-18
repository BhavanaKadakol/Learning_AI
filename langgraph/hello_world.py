from langgraph.graph import MessagesState, StateGraph, START,END

def call_llm(state: MessagesState):
  return {"messages": [{"role": "assistant", "content": "Hello, world!"}]}

graph = StateGraph(MessagesState)
graph.add_node(call_llm)
graph.add_edge(START, "call_llm")
graph.add_edge("call_llm", END)
graph = graph.compile()

result = graph.invoke({"messages": [{"role": "user", "content": "Hello, how are you?"}]})
print(result)
