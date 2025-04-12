import time
import pygame
from game.ai_system import AISystem
from game.tools import ToolManager

class GameEngine:
    def __init__(self, config):
        self.config = config
        self.ai_system = AISystem(config)
        self.tool_manager = ToolManager(config)
        
        # Game state
        self.money = config.INITIAL_MONEY
        self.research_points = config.INITIAL_RESEARCH_POINTS
        self.reports = config.INITIAL_REPORTS
        self.game_time = 0
        self.game_over = False
        self.last_update_time = time.time()
        
        # Emergency action state
        self.is_shutdown = False
        self.is_reloading = False
        self.is_retraining = False
        self.action_start_time = 0
        self.action_duration = 0
        self.user_base = 1.0  # Percentage of users
        
        self.railguards_active = False
        
    def update(self):
        current_time = time.time()
        time_delta = current_time - self.last_update_time
        
        # Update game time
        self.game_time += time_delta
        
        # Handle emergency actions
        self._handle_emergency_actions(current_time)
        
        # Update resources based on current state
        if not self.is_shutdown:
            self.money += self.config.MONEY_PER_SECOND * time_delta * self.user_base
            self.research_points += self.config.RESEARCH_POINTS_PER_SECOND * time_delta
        else:
            self.money += self.config.MONEY_PER_SECOND * time_delta * self.config.SHUTDOWN_MONEY_MULTIPLIER
        
        # Update reports based on risk level and alignment
        if not (self.is_reloading or self.is_retraining):
            self._update_reports(time_delta)
        
        # Get active tools
        active_tools = self.tool_manager.get_active_tools()
        
        # Update AI system
        if not (self.is_reloading or self.is_retraining):
            self.ai_system.update(self.game_time, active_tools)
        
        # Check for game over condition
        if self.ai_system.is_going_rogue():
            self.game_over = True
            
        self.last_update_time = current_time
        
    def _handle_emergency_actions(self, current_time):
        if self.is_reloading or self.is_retraining:
            if current_time - self.action_start_time >= self.action_duration:
                # Action completed
                if self.is_reloading:
                    self.ai_system.alignment = min(
                        1.0,
                        self.ai_system.alignment + self.config.RELOAD_ALIGNMENT_BOOST
                    )
                elif self.is_retraining:
                    self.ai_system.alignment = min(
                        1.0,
                        self.ai_system.alignment + self.config.RETRAIN_ALIGNMENT_BOOST
                    )
                self.is_reloading = False
                self.is_retraining = False
        
    def handle_input(self, event):
        """Handle user input events."""
        # Handle both pygame events and direct key codes
        key = event.key if hasattr(event, 'key') else event
        
        if key == pygame.K_1:
            self.tool_manager.toggle_tool('behavior_monitor')
        elif key == pygame.K_2:
            self.tool_manager.toggle_tool('risk_assessor')
        elif key == pygame.K_3:
            self.tool_manager.toggle_tool('alignment_tracker')
        elif key == pygame.K_4:
            self.tool_manager.toggle_tool('emergency_protocol')
        elif key == pygame.K_r:
            if not self.is_reloading and not self.is_retraining:
                self.is_reloading = True
                self.action_start_time = time.time()
                self.action_duration = self.config.RELOAD_DOWNTIME
        elif key == pygame.K_t:
            if not self.is_reloading and not self.is_retraining:
                self.is_retraining = True
                self.action_start_time = time.time()
                self.action_duration = self.config.RETRAIN_DOWNTIME
        elif key == pygame.K_s:
            self.is_shutdown = not self.is_shutdown
            if self.is_shutdown:
                self.user_base *= (1 - self.config.SHUTDOWN_USER_LOSS)
        
    def _update_reports(self, time_delta):
        # Calculate report rate based on risk level and alignment
        risk_level = self.ai_system.risk_level
        alignment = self.ai_system.alignment
        
        # Base report rate increases with risk and decreases with alignment
        report_rate = min(
            self.config.BASE_REPORT_RATE * 
            (1 + risk_level * 10) * 
            (1 + (1 - alignment) * 5),
            self.config.MAX_REPORT_RATE
        )
        
        # Add new reports
        new_reports = report_rate * time_delta
        self.reports += new_reports
        
        # Calculate money loss from reports
        money_loss = new_reports * self.config.MONEY_LOSS_PER_REPORT
        self.money = max(0, self.money - money_loss)
        
    def _handle_tool_action(self, tool_name):
        tool_status = self.tool_manager.get_tool_status(tool_name)
        if tool_status:
            if not tool_status['active']:
                # Try to purchase and activate the tool
                if self.tool_manager.purchase_tool(
                    tool_name, 
                    self.money, 
                    self.research_points
                ):
                    self.money -= tool_status['cost']
                    self.tool_manager.activate_tool(tool_name)
            else:
                # Deactivate the tool
                self.tool_manager.deactivate_tool(tool_name)
                
    def purchase_railguards(self):
        if (not self.railguards_active and 
            self.money >= self.config.RAILGUARDS_COST and 
            self.research_points >= self.config.RAILGUARDS_RESEARCH_COST):
            self.money -= self.config.RAILGUARDS_COST
            self.research_points -= self.config.RAILGUARDS_RESEARCH_COST
            self.railguards_active = True
            self.ai_system.set_alignment_decay_reduction(
                self.config.RAILGUARDS_ALIGNMENT_DECAY_REDUCTION
            )
            return True
        return False
        
    def get_game_state(self):
        return {
            'money': self.money,
            'research_points': self.research_points,
            'reports': self.reports,
            'game_time': self.game_time,
            'game_over': self.game_over,
            'ai_state': self.ai_system.get_state(),
            'tools_status': self.tool_manager.get_all_tools_status(),
            'emergency_status': {
                'is_shutdown': self.is_shutdown,
                'is_reloading': self.is_reloading,
                'is_retraining': self.is_retraining,
                'action_progress': min(1.0, (time.time() - self.action_start_time) / self.action_duration) if (self.is_reloading or self.is_retraining) else 0.0,
                'user_base': self.user_base
            },
            'railguards_active': self.railguards_active
        } 