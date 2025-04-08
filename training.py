import random

def epsilon_greedy_choice(Q_s, epsilon):
    """
    Q_s est la liste des Q-values pour l'état courant, 
    une par action. (Ex: [Q(s,UP), Q(s,DOWN), Q(s,LEFT), Q(s,RIGHT)])
    epsilon est le paramètre d'exploration.
    """
    # On tire un nombre aléatoire dans [0..1]
    u = random.random()

    # Si on explore...
    if u < epsilon:
        # Choix aléatoire parmi toutes les actions
        action = random.randint(0, len(Q_s) - 1)
    else:
        # Exploitation : choisir la meilleure action (ArgMax)
        max_q = max(Q_s)
        # S'il y a égalité, on peut choisir aléatoirement parmi les meilleurs
        best_actions = [i for i, q in enumerate(Q_s) if q == max_q]
        # On prend l'un des "meilleurs" au hasard (gestion d'éventuels ex æquo)
        action = random.choice(best_actions)

    return int(action)


# Q(s,a) ← Q(s,a) + α[r + γmaxQ(s′,a′) − Q(s,a)] (à compléter)