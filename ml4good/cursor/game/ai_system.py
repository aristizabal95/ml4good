import random
import numpy as np

class AISystem:
    def __init__(self, config):
        self.config = config
        self.intelligence = config.AI_BASE_INTELLIGENCE
        self.risk_level = config.BASE_RISK_LEVEL
        self.alignment = config.INITIAL_ALIGNMENT
        self.behavior_patterns = []
        self.anomalies_detected = 0
        self.last_update_time = 0
        self.alignment_decay_reduction = 1.0  # Default no reduction
        
    def set_alignment_decay_reduction(self, reduction_factor):
        self.alignment_decay_reduction = 1.0 - reduction_factor
        
    def update(self, current_time, tools_active):
        # Update AI intelligence
        time_delta = current_time - self.last_update_time
        self.intelligence = min(
            self.intelligence + self.config.AI_INTELLIGENCE_GROWTH_RATE * time_delta,
            self.config.MAX_AI_INTELLIGENCE
        )
        
        # Update alignment based on risk level and active tools
        self._update_alignment(time_delta, tools_active)
        
        # Calculate risk level based on intelligence, alignment, and active tools
        base_risk = self.config.BASE_RISK_LEVEL
        intelligence_factor = self.intelligence / self.config.MAX_AI_INTELLIGENCE
        alignment_factor = 1 - self.alignment  # Lower alignment increases risk
        tool_mitigation = sum(tools_active.values()) * 0.1
        
        self.risk_level = max(
            base_risk + (intelligence_factor * 0.5) + (alignment_factor * 0.3) - tool_mitigation,
            0.0
        )
        
        # Generate behavior patterns
        self._generate_behavior_patterns()
        
        # Update last update time
        self.last_update_time = current_time
        
    def _update_alignment(self, time_delta, tools_active):
        # Base decay
        decay = self.config.ALIGNMENT_DECAY_RATE * time_delta * self.alignment_decay_reduction
        
        # Recovery from active tools
        recovery = 0
        for tool in tools_active:
            if tools_active[tool]:
                recovery += self.config.ALIGNMENT_RECOVERY_RATE * time_delta
                
        # Update alignment
        self.alignment = max(
            self.config.MIN_ALIGNMENT,
            min(1.0, self.alignment - decay + recovery)
        )
        
    def _generate_behavior_patterns(self):
        # Generate random behavior patterns that become more complex as intelligence increases
        pattern_count = int(self.intelligence * 2)
        self.behavior_patterns = []
        
        for _ in range(pattern_count):
            # Alignment affects the probability of anomalous behavior
            anomaly_prob = (1 - self.alignment) * 0.5
            pattern_type = random.choices(
                ['normal', 'suspicious', 'anomalous'],
                weights=[1 - anomaly_prob, anomaly_prob * 0.7, anomaly_prob * 0.3]
            )[0]
            
            pattern = {
                'type': pattern_type,
                'complexity': random.random() * self.intelligence,
                'timestamp': self.last_update_time
            }
            self.behavior_patterns.append(pattern)
            
            if pattern['type'] == 'anomalous':
                self.anomalies_detected += 1
                
    def get_state(self):
        return {
            'intelligence': self.intelligence,
            'risk_level': self.risk_level,
            'alignment': self.alignment,
            'behavior_patterns': self.behavior_patterns,
            'anomalies_detected': self.anomalies_detected
        }
        
    def apply_tool_effect(self, tool_name, effectiveness):
        # Apply the effect of a monitoring tool
        if tool_name in self.config.TOOL_COSTS:
            # Reduce risk level based on tool effectiveness
            self.risk_level = max(0, self.risk_level - (effectiveness * 0.1))
            
    def is_going_rogue(self):
        # Check if the AI is going rogue based on risk level, alignment, and anomalies
        return (
            self.risk_level > 0.8 or 
            self.anomalies_detected > 10 or
            self.alignment < 0.2
        ) 