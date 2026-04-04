from langgraph.graph import StateGraph
from src.langgraphagenticai.state.state import State
from langgraph.graph import START,END
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from langgraph.prebuilt import tools_condition,ToolNode
from src.langgraphagenticai.tools.search_tool import get_tools,create_tool_node
from src.langgraphagenticai.nodes.ai_news_node import AINewsNode

from src.langgraphagenticai.nodes.chatbot_with_tool_node import ChatbotWithToolNode
class GraphBuilder:
    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(State)
        
    def basic_chatbot_build_graph(self):
         """
        Builds a basic chatbot graph using LangGraph.
        This method initializes a chatbot node using the `BasicChatbotNode` class 
        and integrates it into the graph. The chatbot node is set as both the 
        entry and exit point of the graph.
         """
 
         self.basic_chatbot_node=BasicChatbotNode(self.llm)

         self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
         self.graph_builder.add_edge(START,"chatbot")
         self.graph_builder.add_edge("chatbot",END)
         
    def chatbot_with_tools_build_graph(self):
        """"
                Builds an advanced chatbot graph with tool integration.
        This method creates a chatbot graph that includes both a chatbot node 
        and a tool node. It defines tools, initializes the chatbot with tool 
        capabilities, and sets up conditional and direct edges between nodes. 
        The chatbot node is set as the entry point.
        """
        # define the tool and tool node 
        tools=get_tools()
        tool_node=create_tool_node(tools)
        
        # define the llm
        llm=self.llm
        
        # define the chatbot node with tool using the llm and tool node

        
        obj_chatbot_with_node=ChatbotWithToolNode(llm)
        chatbot_node=obj_chatbot_with_node.create_chatbot(tools)
        # add nodes
        
        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools",tool_node)
        
        # define condition and direct edges
        
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge("tools","chatbot")
        self.graph_builder.add_edge("chatbot",END)
        
        
    def ai_news_builder_graph(self):
        """
        Builds a graph for an AI news use case.
        This method is a placeholder for constructing a graph tailored to an AI news application. 
        It can be expanded to include specific nodes and edges relevant to the use case.
        """
        # add nodes and edges for AI news use case
        
        
        ai_news_node=AINewsNode(self.llm)
        
        
        self.graph_builder.add_node("fetch_news", ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news", ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result", ai_news_node.save_result)
        
        
        self.graph_builder.add_edge(START,"fetch_news")
        self.graph_builder.add_edge("fetch_news","summarize_news")
        self.graph_builder.add_edge("summarize_news","save_result")
        self.graph_builder.add_edge("save_result",END)
        
        
    def setup_graph(self, usecase: str):
        """
        Sets up the graph for the selected use case.
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
            
        if usecase == "Chatbot With Web":
            self.chatbot_with_tools_build_graph()
            
        if usecase == "AI News":
            self.ai_news_builder_graph()

        return self.graph_builder.compile()
