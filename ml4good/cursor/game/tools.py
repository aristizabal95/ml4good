class MonitoringTool:
    def __init__(self, name, cost, research_required, effectiveness):
        self.name = name
        self.cost = cost
        self.research_required = research_required
        self.effectiveness = effectiveness
        self.is_active = False
        self.energy_consumption = 0.1  # Base energy consumption
        
    def activate(self):
        self.is_active = True
        
    def deactivate(self):
        self.is_active = False
        
    def get_status(self):
        return {
            'name': self.name,
            'active': self.is_active,
            'effectiveness': self.effectiveness,
            'energy_consumption': self.energy_consumption
        }


class ToolManager:
    def __init__(self, config):
        self.config = config
        self.tools = {}
        self._initialize_tools()
        
    def _initialize_tools(self):
        # Initialize all available tools
        self.tools = {
            'basic_monitor': MonitoringTool(
                'Basic Monitor',
                self.config.TOOL_COSTS['basic_monitor'],
                self.config.TOOL_RESEARCH_REQUIREMENTS['basic_monitor'],
                0.2
            ),
            'advanced_monitor': MonitoringTool(
                'Advanced Monitor',
                self.config.TOOL_COSTS['advanced_monitor'],
                self.config.TOOL_RESEARCH_REQUIREMENTS['advanced_monitor'],
                0.4
            ),
            'automated_analysis': MonitoringTool(
                'Automated Analysis',
                self.config.TOOL_COSTS['automated_analysis'],
                self.config.TOOL_RESEARCH_REQUIREMENTS['automated_analysis'],
                0.6
            ),
            'predictive_system': MonitoringTool(
                'Predictive System',
                self.config.TOOL_COSTS['predictive_system'],
                self.config.TOOL_RESEARCH_REQUIREMENTS['predictive_system'],
                0.8
            ),
            'emergency_protocol': MonitoringTool(
                'Emergency Protocol',
                self.config.TOOL_COSTS['emergency_protocol'],
                self.config.TOOL_RESEARCH_REQUIREMENTS['emergency_protocol'],
                1.0
            )
        }
        
    def purchase_tool(self, tool_name, money, research_points):
        if tool_name in self.tools:
            tool = self.tools[tool_name]
            if (money >= tool.cost and 
                research_points >= tool.research_required):
                return True
        return False
        
    def activate_tool(self, tool_name):
        if tool_name in self.tools:
            self.tools[tool_name].activate()
            return True
        return False
        
    def deactivate_tool(self, tool_name):
        if tool_name in self.tools:
            self.tools[tool_name].deactivate()
            return True
        return False
        
    def get_active_tools(self):
        return {
            name: tool.is_active 
            for name, tool in self.tools.items()
        }
        
    def get_tool_status(self, tool_name):
        if tool_name in self.tools:
            return self.tools[tool_name].get_status()
        return None
        
    def get_all_tools_status(self):
        return {
            name: tool.get_status() 
            for name, tool in self.tools.items()
        } 