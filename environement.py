import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import time



class GridWorld:
    def __init__(self, width=4, height=3, cell_width=120, cell_height=120):
        # --- Paramètres de la grille ---
        self.GRID_WIDTH = width
        self.GRID_HEIGHT = height
        self.CELL_W = cell_width
        self.CELL_H = cell_height
        
        # Q-table stockée aussi dans la session, pour avoir 4 Q-values par case
        # On peut initialiser tout à zéro, ou de manière aléatoire
        if "Q" not in st.session_state:
            # Q[x][y] = [q_up, q_down, q_left, q_right]
            st.session_state.Q = [
                [
                    [0.0, 0.0, 0.0, 0.0] for _ in range(self.GRID_HEIGHT)
                ]
                for _ in range(self.GRID_WIDTH)
            ]
        
        # Positions spéciales :
        self.goal_pos = (3, 2)    # But (vert)
        self.danger_pos = (3, 1)  # Danger (rouge)
        self.wall_pos = (1, 1)    # Mur (gris)



    def reset_position(self):
        """Réinitialise la position de l'agent à (0,0)."""
        st.session_state.agent_pos = (0, 0)

    def color_for_q(self, q_value):
        """
        Convertit une Q-value dans [-1..1] en une couleur
        du rouge (val. négatives) au vert (val. positives).
        """
        q = max(-1, min(1, q_value))  # borne
        t = (q + 1) / 2.0             # [0..1]
        r = int(255 * (1 - t))
        g = int(255 * t)
        b = 0
        return (r, g, b)

    def triangle_points(self, action, x1, y1, x2, y2):
        """
        0=UP, 1=DOWN, 2=LEFT, 3=RIGHT.
        Le "sommet" (apex) est au centre (cx, cy).
        La "base" sur le bord correspondant.
        """
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        if action == 0:  # UP
            return [(x1, y1), (x2, y1), (cx, cy)]
        elif action == 1:  # DOWN
            return [(x1, y2), (x2, y2), (cx, cy)]
        elif action == 2:  # LEFT
            return [(x1, y1), (x1, y2), (cx, cy)]
        elif action == 3:  # RIGHT
            return [(x2, y1), (x2, y2), (cx, cy)]

    def dessiner_grille(self, placeholder,  position=(0,0)):
        """
        Crée l'image PIL de la grille 4x3,
        - but en vert,
        - danger en rouge,
        - mur en gris,
        - 4 triangles par case colorés selon Q,
        - et l'agent en bleu.
        """
        img_w = self.GRID_WIDTH * self.CELL_W
        img_h = self.GRID_HEIGHT * self.CELL_H
        img = Image.new("RGB", (img_w, img_h), "white")
        draw = ImageDraw.Draw(img)

        # Police par défaut (pour afficher la valeur des triangles)
        font = ImageFont.load_default()

        for y in range(self.GRID_HEIGHT):
            for x in range(self.GRID_WIDTH):
                screen_y = self.GRID_HEIGHT - 1 - y
                x1 = x * self.CELL_W
                y1 = screen_y * self.CELL_H
                x2 = x1 + self.CELL_W
                y2 = y1 + self.CELL_H

                # Déterminer la couleur de fond
                if (x, y) == self.goal_pos:
                    cell_color = (144, 238, 144)  # lightgreen
                elif (x, y) == self.danger_pos:
                    cell_color = (240, 128, 128)  # lightcoral
                elif (x, y) == self.wall_pos:
                    cell_color = (211, 211, 211)  # lightgray
                else:
                    cell_color = (255, 255, 255)  # white

                # Dessin du rectangle
                draw.rectangle([x1, y1, x2, y2],
                            outline="black", width=2, fill=cell_color)

                # Dessiner 4 triangles si ce n'est pas mur / goal / danger
                if (x, y) not in [self.wall_pos, self.goal_pos, self.danger_pos]:
                    # Récupérer les Q-values associées à la case (x,y)
                    # Q[x][y] = [q_up, q_down, q_left, q_right]
                    qvals = st.session_state.Q[x][y]

                    for action_idx in range(4):
                        tri = self.triangle_points(action_idx, x1, y1, x2, y2)
                        qval = qvals[action_idx]

                        # Couleur du triangle en fonction de la Q-value
                        color_tri = self.color_for_q(qval)

                        # Dessin du triangle
                        draw.polygon(tri, fill=color_tri, outline="black")

                        # Affichage de la Q-value en texte
                        cx = sum([p[0] for p in tri]) / 3.0
                        cy = sum([p[1] for p in tri]) / 3.0
                        draw.text((cx - 6, cy - 5), f"{qval:.2f}",
                                fill="black", font=font)

        # Dessin de l'agent (cercle bleu)
        agent_x, agent_y = st.session_state.agent_pos
        screen_yA = self.GRID_HEIGHT - 1 - agent_y
        ax1 = agent_x * self.CELL_W
        ay1 = screen_yA * self.CELL_H
        ax2 = ax1 + self.CELL_W
        ay2 = ay1 + self.CELL_H

        # On dessine un cercle au centre de la cellule
        padding = 30
        draw.ellipse([ax1+padding, ay1+padding, ax2-padding, ay2-padding],
                    fill="blue", outline="black", width=3)

        placeholder.image(img, caption=f"Position de l'agent : {str(position)}")