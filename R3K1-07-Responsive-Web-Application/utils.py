import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

def format_time(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{int(minutes)}:{int(remaining_seconds):02d}"

def create_physics_diagram(diagram_type, params):
    plt.figure(figsize=(6, 4))
    
    if diagram_type == "projectile":
        t = np.linspace(0, params['time'], 100)
        x = params['v0'] * np.cos(params['angle']) * t
        y = params['v0'] * np.sin(params['angle']) * t - 0.5 * 9.81 * t**2
        plt.plot(x, y)
        plt.title("Projectile Motion")
        
    elif diagram_type == "pendulum":
        t = np.linspace(0, 10, 1000)
        theta = params['amplitude'] * np.cos(np.sqrt(9.81/params['length']) * t)
        plt.plot(t, theta)
        plt.title("Simple Pendulum")
        
    plt.grid(True)
    plt.xlabel("x")
    plt.ylabel("y")
    return plt

def latex_formula(formula_str):
    return sp.latex(sp.sympify(formula_str))
