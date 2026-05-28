import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Título de la aplicación
st.set_page_config(page_title="Simulador de Perceptrón", layout="wide")
st.title("🕹️ Tarea 1: Perceptrón Gamificado")
st.markdown("Mueve los sliders para encontrar los pesos que clasifican correctamente los puntos.")

# --- SIDEBAR: CONTROLES ---
st.sidebar.header("🎛️ Perillas del Perceptrón")
w1 = st.sidebar.slider("Peso w1", -2.0, 2.0, 0.5, step=0.1)
w2 = st.sidebar.slider("Peso w2", -2.0, 2.0, -0.5, step=0.1)
bias = st.sidebar.slider("Sesgo (bias)", -2.0, 2.0, 0.0, step=0.1)

# --- CONFIGURACIÓN DE DATOS ---
st.sidebar.divider()
tipo_puerta = st.sidebar.selectbox("Selecciona el problema", ["AND", "OR", "XOR (El imposible)"])

# Definir targets según selección
if tipo_puerta == "AND":
    targets = [0, 0, 0, 1]
elif tipo_puerta == "OR":
    targets = [0, 1, 1, 1]
else:
    targets = [0, 1, 1, 0]

# --- LÓGICA DEL PERCEPTRÓN ---
entradas = np.array([[0,0], [0,1], [1,0], [1,1]])
predicciones = []
aciertos = 0

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Tabla de Clasificación")
    for i, x in enumerate(entradas):
        # Cálculo: z = w1*x1 + w2*x2 + b
        suma_ponderada = w1*x[0] + w2*x[1] + bias
        y_out = 1 if suma_ponderada >= 0 else 0
        predicciones.append(y_out)
        
        es_correcto = "✅" if y_out == targets[i] else "❌"
        if y_out == targets[i]: aciertos += 1
        
        st.write(f"Entrada {x} | Deseado: {targets[i]} | Salida: **{y_out}** {es_correcto}")

    st.metric("Puntuación Final", f"{aciertos} / 4 aciertos")

# --- GRÁFICA ---
with col2:
    st.subheader("📈 Frontera de Decisión")
    fig, ax = plt.subplots()
    
    # Dibujar puntos
    for i, x in enumerate(entradas):
        color = 'blue' if targets[i] == 1 else 'red'
        ax.scatter(x[0], x[1], c=color, s=200, edgecolors='black', zorder=5)
        ax.text(x[0]+0.05, x[1]+0.05, f"({x[0]},{x[1]})")

    # Dibujar la línea: w1*x + w2*y + b = 0  => y = -(w1/w2)x - (b/w2)
    x_vals = np.linspace(-0.5, 1.5, 100)
    if w2 != 0:
        y_vals = -(w1/w2)*x_vals - (bias/w2)
        ax.plot(x_vals, y_vals, label="Línea de decisión", color="green", linewidth=2)
        ax.fill_between(x_vals, y_vals, 2, color='blue', alpha=0.1)
        ax.fill_between(x_vals, y_vals, -2, color='red', alpha=0.1)

    ax.set_xlim([-0.5, 1.5])
    ax.set_ylim([-0.5, 1.5])
    ax.axhline(0, color='black',linewidth=0.5)
    ax.axvline(0, color='black',linewidth=0.5)
    ax.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig)