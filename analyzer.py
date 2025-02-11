import time
import matplotlib.pyplot as plt
import numpy as np
from config_loader import load_config
from turing_machine import TuringMachine

def run_simulation(n, config):
    """
    Ejecuta la simulación para una entrada n.
    
    Se asume que:
      - n es el número de términos (entrada en unaria: por ejemplo, '111' para n=3).
      - Para n>=3 se establece el contador de iteración como '1'*(n-2).
      - Los segmentos A y B se inicializan en "1" (F(1)=F(2)=1).
    """
    if n < 1:
        raise ValueError("n debe ser al menos 1")
    if n <= 2:
        iteration = ""
    else:
        iteration = "1" * (n - 2)
    A = "1"
    B = "1"
    tm = TuringMachine(config, iteration, A, B)
    start = time.perf_counter()
    tm.run()
    end = time.perf_counter()
    elapsed = end - start
    return elapsed

def empirical_analysis(config):
    test_inputs = list(range(1, 21))  
    times = []
    for n in test_inputs:
        t = run_simulation(n, config)
        times.append(t)
        print(f"n = {n}, tiempo = {t:.6f} segundos")
    
    plt.scatter(test_inputs, times, label="Tiempo de ejecución")
    plt.xlabel("Tamaño de entrada (n)")
    plt.ylabel("Tiempo (segundos)")
    plt.title("Tiempo de ejecución vs Tamaño de entrada")
    
    coefficients = np.polyfit(test_inputs, times, 2)
    poly = np.poly1d(coefficients)
    xs = np.linspace(min(test_inputs), max(test_inputs), 100)
    ys = poly(xs)
    plt.plot(xs, ys, color='red', label=f"ajuste: {poly}")
    plt.legend()
    plt.show()
