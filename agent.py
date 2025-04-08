import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import time

class Agent:
    def __init__(self, x, y, gridworld, placeholder):
        self.x = x
        self.y = y
        self.gridworld = gridworld
        self.placeholder = placeholder
        # Position de l'agent stockée dans la session (x, y)
        if "agent_pos" not in st.session_state:
            st.session_state.agent_pos = (0, 0)  # Par défaut (0,0)
        gridworld.dessiner_grille(self.placeholder)

    def can_move(self, x, y):
        """Vérifie si (x,y) est dans la grille et n'est pas la case 'mur'."""
        if 0 <= self.x < self.gridworld.GRID_WIDTH and 0 <= self.y < self.gridworld.GRID_HEIGHT:
            return (self.x, self.y) != self.gridworld.wall_pos
        return False
        

    def move_agent(self, direction):
        """
        Déplace l'agent vers 'up', 'down', 'left' ou 'right'
        si la case est valide (pas hors limite ni mur).
        Met à jour st.session_state.agent_pos.
        """
        self.x, self.y = st.session_state.agent_pos
        if direction == "up":
            new_x, new_y = self.x, self.y + 1
        elif direction == "down":
            new_x, new_y = self.x, self.y - 1
        elif direction == "left":
            new_x, new_y = self.x - 1, self.y
        elif direction == "right":
            new_x, new_y = self.x + 1, self.y
        else:
            return  # Action inconnue

        if self.can_move(new_x, new_y):
            st.session_state.agent_pos = (new_x, new_y)
        self.gridworld.dessiner_grille(self.placeholder, (self.x, self.y))