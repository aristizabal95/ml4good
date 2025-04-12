import pygame
import pygame.font

class GameUI:
    def __init__(self, config):
        self.config = config
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("AI Overseer")
        
        # Initialize fonts
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 36)
        
        # UI elements
        self.status_bar_height = 40
        self.tool_panel_width = 300
        self.emergency_panel_width = 200
        
        # Emergency action buttons
        self.reload_button = pygame.Rect(50, 400, 300, 40)
        self.retrain_button = pygame.Rect(50, 450, 300, 40)
        self.shutdown_button = pygame.Rect(50, 500, 300, 40)
        
        # Railguards button
        self.railguards_button = pygame.Rect(50, 300, 300, 40)
        
    def handle_click(self, pos):
        """Handle mouse click events and return the action if a button was clicked."""
        if self.reload_button.collidepoint(pos):
            return 'reload'
        elif self.retrain_button.collidepoint(pos):
            return 'retrain'
        elif self.shutdown_button.collidepoint(pos):
            return 'shutdown'
        elif self.railguards_button.collidepoint(pos):
            return 'railguards'
        return None
        
    def render(self, game_state):
        # Clear screen
        self.screen.fill(self.config.BACKGROUND_COLOR)
        
        # Draw status bar
        self._draw_status_bar(game_state)
        
        # Draw main game area
        self._draw_main_area(game_state)
        
        # Draw tool panel
        self._draw_tool_panel(game_state)
        
        # Draw emergency actions
        self._draw_emergency_actions(game_state)
        
        # Update display
        pygame.display.flip()
        
    def _draw_status_bar(self, game_state):
        # Draw status bar background
        pygame.draw.rect(
            self.screen,
            (40, 40, 40),
            (0, 0, self.config.SCREEN_WIDTH, self.status_bar_height)
        )
        
        # Draw money and research points
        money_text = self.font.render(
            f"Money: ${int(game_state['money'])}",
            True,
            self.config.TEXT_COLOR
        )
        research_text = self.font.render(
            f"Research: {int(game_state['research_points'])}",
            True,
            self.config.TEXT_COLOR
        )
        
        # Draw reports
        reports_color = self._get_reports_color(game_state['reports'])
        reports_text = self.font.render(
            f"Reports: {int(game_state['reports'])}",
            True,
            reports_color
        )
        
        # Draw alignment
        alignment_color = self._get_alignment_color(
            game_state['ai_state']['alignment']
        )
        alignment_text = self.font.render(
            f"Alignment: {game_state['ai_state']['alignment']:.2f}",
            True,
            alignment_color
        )
        
        self.screen.blit(money_text, (10, 10))
        self.screen.blit(research_text, (200, 10))
        self.screen.blit(reports_text, (400, 10))
        self.screen.blit(alignment_text, (600, 10))
        
    def _draw_main_area(self, game_state):
        # Draw AI status
        ai_state = game_state['ai_state']
        title = self.title_font.render(
            "AI System Status",
            True,
            self.config.TEXT_COLOR
        )
        self.screen.blit(title, (50, 60))
        
        # Draw intelligence level
        intel_text = self.font.render(
            f"Intelligence: {ai_state['intelligence']:.2f}",
            True,
            self.config.TEXT_COLOR
        )
        self.screen.blit(intel_text, (50, 110))
        
        # Draw alignment impact
        alignment_impact = self.font.render(
            f"Alignment Impact: {self._get_alignment_impact_text(ai_state['alignment'])}",
            True,
            self._get_alignment_color(ai_state['alignment'])
        )
        self.screen.blit(alignment_impact, (50, 140))
        
        # Draw behavior patterns
        pattern_text = self.font.render(
            f"Anomalies Detected: {ai_state['anomalies_detected']}",
            True,
            self.config.TEXT_COLOR
        )
        self.screen.blit(pattern_text, (50, 170))
        
        # Draw reports impact
        impact_text = self.font.render(
            f"Money Loss from Reports: ${int(game_state['reports'] * self.config.MONEY_LOSS_PER_REPORT)}",
            True,
            self._get_reports_color(game_state['reports'])
        )
        self.screen.blit(impact_text, (50, 200))
        
        # Draw Railguards button
        if not game_state['railguards_active']:
            railguards_color = (0, 200, 255)  # Light blue
            pygame.draw.rect(self.screen, railguards_color, self.railguards_button)
            railguards_text = self.font.render(
                f"Buy Railguards (G) ${self.config.RAILGUARDS_COST}",
                True,
                (0, 0, 0)
            )
            self.screen.blit(railguards_text, (self.railguards_button.x + 10, self.railguards_button.y + 10))
        else:
            railguards_text = self.font.render(
                "Railguards Active",
                True,
                (0, 200, 255)
            )
            self.screen.blit(railguards_text, (50, 310))
        
    def _draw_emergency_actions(self, game_state):
        emergency_status = game_state['emergency_status']
        
        # Draw emergency panel title
        title = self.title_font.render(
            "Emergency Actions",
            True,
            self.config.TEXT_COLOR
        )
        self.screen.blit(title, (50, 350))
        
        # Draw reload button
        reload_color = (0, 255, 0) if not emergency_status['is_reloading'] else (100, 100, 100)
        pygame.draw.rect(self.screen, reload_color, self.reload_button)
        reload_text = self.font.render(
            "Reload (R)" if not emergency_status['is_reloading'] else f"Reloading... {int(emergency_status['action_progress'] * 100)}%",
            True,
            (0, 0, 0)
        )
        self.screen.blit(reload_text, (self.reload_button.x + 10, self.reload_button.y + 10))
        
        # Draw retrain button
        retrain_color = (255, 165, 0) if not emergency_status['is_retraining'] else (100, 100, 100)
        pygame.draw.rect(self.screen, retrain_color, self.retrain_button)
        retrain_text = self.font.render(
            "Retrain (T)" if not emergency_status['is_retraining'] else f"Retraining... {int(emergency_status['action_progress'] * 100)}%",
            True,
            (0, 0, 0)
        )
        self.screen.blit(retrain_text, (self.retrain_button.x + 10, self.retrain_button.y + 10))
        
        # Draw shutdown button
        shutdown_color = (255, 0, 0) if not emergency_status['is_shutdown'] else (100, 100, 100)
        pygame.draw.rect(self.screen, shutdown_color, self.shutdown_button)
        shutdown_text = self.font.render(
            "Shutdown (S)" if not emergency_status['is_shutdown'] else "Restart (S)",
            True,
            (0, 0, 0)
        )
        self.screen.blit(shutdown_text, (self.shutdown_button.x + 10, self.shutdown_button.y + 10))
        
        # Draw user base status
        user_text = self.font.render(
            f"User Base: {int(emergency_status['user_base'] * 100)}%",
            True,
            self.config.TEXT_COLOR
        )
        self.screen.blit(user_text, (50, 550))
        
    def _draw_tool_panel(self, game_state):
        # Draw tool panel background
        pygame.draw.rect(
            self.screen,
            (30, 30, 30),
            (
                self.config.SCREEN_WIDTH - self.tool_panel_width,
                0,
                self.tool_panel_width,
                self.config.SCREEN_HEIGHT
            )
        )
        
        # Draw tool panel title
        title = self.title_font.render(
            "Monitoring Tools",
            True,
            self.config.TEXT_COLOR
        )
        self.screen.blit(
            title,
            (self.config.SCREEN_WIDTH - self.tool_panel_width + 10, 60)
        )
        
        # Draw tools
        y_offset = 120
        for tool_name, tool_status in game_state['tools_status'].items():
            color = (0, 255, 0) if tool_status['active'] else (255, 0, 0)
            tool_text = self.font.render(
                f"{tool_name}: {'Active' if tool_status['active'] else 'Inactive'}",
                True,
                color
            )
            self.screen.blit(
                tool_text,
                (self.config.SCREEN_WIDTH - self.tool_panel_width + 10, y_offset)
            )
            y_offset += 30
            
    def _get_risk_color(self, risk_level):
        if risk_level < 0.3:
            return (0, 255, 0)  # Green
        elif risk_level < 0.6:
            return (255, 165, 0)  # Orange
        else:
            return (255, 0, 0)  # Red
            
    def _get_reports_color(self, reports):
        threshold = self.config.REPORT_THRESHOLD
        if reports < threshold * 0.3:
            return (0, 255, 0)  # Green
        elif reports < threshold * 0.6:
            return (255, 165, 0)  # Orange
        else:
            return (255, 0, 0)  # Red
            
    def _get_alignment_color(self, alignment):
        if alignment > 0.7:
            return (0, 255, 0)  # Green
        elif alignment > 0.4:
            return (255, 165, 0)  # Orange
        else:
            return (255, 0, 0)  # Red
            
    def _get_alignment_impact_text(self, alignment):
        if alignment > 0.8:
            return "Excellent"
        elif alignment > 0.6:
            return "Good"
        elif alignment > 0.4:
            return "Concerning"
        elif alignment > 0.2:
            return "Critical"
        else:
            return "Emergency" 