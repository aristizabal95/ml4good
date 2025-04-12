class GameConfig:
    def __init__(self):
        # Screen settings
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.FPS = 60
        
        # Colors
        self.BACKGROUND_COLOR = (20, 20, 20)
        self.TEXT_COLOR = (255, 255, 255)
        self.WARNING_COLOR = (255, 165, 0)
        self.DANGER_COLOR = (255, 0, 0)
        
        # Game settings
        self.INITIAL_MONEY = 1000
        self.INITIAL_RESEARCH_POINTS = 0
        self.BASE_RISK_LEVEL = 0.3
        self.RISK_INCREASE_RATE = 0.05
        self.MONEY_PER_SECOND = 20
        self.RESEARCH_POINTS_PER_SECOND = 2
        
        # Alignment settings
        self.INITIAL_ALIGNMENT = 1.0
        self.MIN_ALIGNMENT = 0.0
        self.ALIGNMENT_DECAY_RATE = 0.01
        self.ALIGNMENT_RECOVERY_RATE = 0.005
        
        # Emergency actions settings
        self.RELOAD_DOWNTIME = 5.0  # seconds
        self.RELOAD_ALIGNMENT_BOOST = 0.3
        self.RETRAIN_DOWNTIME = 15.0  # seconds
        self.RETRAIN_ALIGNMENT_BOOST = 0.7
        self.SHUTDOWN_USER_LOSS = 0.5  # 50% of users lost
        self.SHUTDOWN_MONEY_MULTIPLIER = 0.0  # No money generation during shutdown
        
        # Reporting system settings
        self.INITIAL_REPORTS = 0
        self.BASE_REPORT_RATE = 0.5
        self.MAX_REPORT_RATE = 20.0
        self.MONEY_LOSS_PER_REPORT = 5
        self.REPORT_THRESHOLD = 500
        
        # AI settings
        self.AI_BASE_INTELLIGENCE = 1.0
        self.AI_INTELLIGENCE_GROWTH_RATE = 0.01
        self.MAX_AI_INTELLIGENCE = 10.0
        
        # Tool settings
        self.TOOL_COSTS = {
            'basic_monitor': 500,
            'advanced_monitor': 2000,
            'automated_analysis': 5000,
            'predictive_system': 10000,
            'emergency_protocol': 20000
        }
        
        self.TOOL_RESEARCH_REQUIREMENTS = {
            'basic_monitor': 0,
            'advanced_monitor': 50,
            'automated_analysis': 200,
            'predictive_system': 500,
            'emergency_protocol': 1000
        }
        
        # Railguards feature
        self.RAILGUARDS_COST = 1000  # Money cost
        self.RAILGUARDS_RESEARCH_COST = 50  # Research points cost
        self.RAILGUARDS_ALIGNMENT_DECAY_REDUCTION = 0.5  # Reduces alignment decay by 50% 