from langgraph.graph import StateGraph, START, END
from .agents import (
    GraphState, 
    segregator_agent, 
    id_agent, 
    discharge_summary_agent, 
    itemized_bill_agent, 
    aggregator_node
)

def create_workflow():
    workflow = StateGraph(GraphState)

    # Add Nodes
    workflow.add_node("segregator", segregator_agent)
    workflow.add_node("id_agent", id_agent)
    workflow.add_node("discharge_agent", discharge_summary_agent)
    workflow.add_node("bill_agent", itemized_bill_agent)
    workflow.add_node("aggregator", aggregator_node)

    # Define Edges
    workflow.add_edge(START, "segregator")
    
    # After segregation, we go to ALL three extraction agents in parallel
    workflow.add_edge("segregator", "id_agent")
    workflow.add_edge("segregator", "discharge_agent")
    workflow.add_edge("segregator", "bill_agent")
    
    # All extraction agents go to aggregator
    workflow.add_edge("id_agent", "aggregator")
    workflow.add_edge("discharge_agent", "aggregator")
    workflow.add_edge("bill_agent", "aggregator")
    
    workflow.add_edge("aggregator", END)

    return workflow.compile()

app_graph = create_workflow()
