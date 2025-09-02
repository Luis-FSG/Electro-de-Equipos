import streamlit as st
import random
import math
import pandas as pd

st.set_page_config(page_title="Distribuidor de Equipos", layout="wide")

st.title("🏆 Distribuidor de Equipos Balanceados - Versión Web")

# Datos iniciales
datos_iniciales = [
    {"nombre": "Clavo", "valor": 3},
    {"nombre": "Bebé", "valor": 1},
    {"nombre": "vete", "valor": 1},
    {"nombre": "gocho", "valor": 2},
    {"nombre": "Víctor", "valor": 3},
    {"nombre": "osmer", "valor": 1},
    {"nombre": "Pablo", "valor": 3},
    {"nombre": "Jesús Clavijo", "valor": 1},
    {"nombre": "oscar", "valor": 3},
    {"nombre": "Brandon", "valor": 3},
    {"nombre": "Eleaking", "valor": 2},
    {"nombre": "Gregory", "valor": 2},
    {"nombre": "Toño", "valor": 3},
    {"nombre": "Hansell", "valor": 1},
    {"nombre": "Chino", "valor": 1},
    {"nombre": "burete", "valor": 2},
    {"nombre": "hassan", "valor": 2},
    {"nombre": "kassem", "valor": 3},
    {"nombre": "Isma", "valor": 3},
    {"nombre": "gary", "valor": 1},
    {"nombre": "Molina", "valor": 2}
]

# Interfaz para editar participantes
st.header("👥 Gestión de Participantes")

if 'datos' not in st.session_state:
    st.session_state.datos = datos_iniciales.copy()

# Mostrar tabla editable
df = pd.DataFrame(st.session_state.datos)
edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

# Botones de acción
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("💾 Guardar Cambios"):
        st.session_state.datos = edited_df.to_dict('records')
        st.success("Cambios guardados!")
        
with col2:
    if st.button("🎲 Distribuir Aleatoriamente"):
        st.session_state.modo = "aleatorio"
        st.rerun()
        
with col3:
    if st.button("⚖️ Distribuir Balanceado"):
        st.session_state.modo = "balanceado"
        st.rerun()

# Función de distribución
def distribuir_equipos(datos, aleatorio=True):
    participantes = datos.copy()
    tamano_equipo = 7
    num_equipos = math.ceil(len(participantes) / tamano_equipo)
    
    if aleatorio:
        random.shuffle(participantes)
        equipos = []
        for i in range(0, len(participantes), tamano_equipo):
            equipo = participantes[i:i + tamano_equipo]
            equipos.append(equipo)
    else:
        participantes.sort(key=lambda x: x['valor'], reverse=True)
        equipos = [[] for _ in range(num_equipos)]
        valores_equipos = [0] * num_equipos
        
        for participante in participantes:
            equipo_idx = valores_equipos.index(min(valores_equipos))
            equipos[equipo_idx].append(participante)
            valores_equipos[equipo_idx] += participante['valor']
    
    return equipos

# Mostrar resultados si se solicitó
if hasattr(st.session_state, 'modo'):
    st.header("📊 Resultados de la Distribución")
    
    equipos = distribuir_equipos(st.session_state.datos, st.session_state.modo == "aleatorio")
    
    # Mostrar equipos en columnas
    cols = st.columns(len(equipos))
    
    stats = []
    for i, equipo in enumerate(equipos):
        with cols[i]:
            total_valor = sum(p["valor"] for p in equipo)
            promedio = total_valor / len(equipo)
            stats.append({"equipo": i+1, "total": total_valor, "promedio": promedio})
            
            st.subheader(f"Equipo {i+1}")
            for participante in equipo:
                iconos = "⚡" * participante["valor"]
                st.write(f"**{participante['nombre']}**: {iconos}")
            
            st.metric("Valor Total", total_valor)
            st.metric("Promedio", f"{promedio:.2f}")
    
    # Estadísticas generales
    st.header("📈 Estadísticas Generales")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Diferencia Máxima", max(s['total'] for s in stats) - min(s['total'] for s in stats))
    
    with col2:
        st.metric("Promedio General", f"{sum(s['total'] for s in stats) / sum(len(equipo) for equipo in equipos):.2f}")
    
    with col3:
        st.metric("Total Participantes", sum(len(equipo) for equipo in equipos))

# Instrucciones
st.sidebar.header("📋 Instrucciones")
st.sidebar.write("""
1. **Edita** los nombres y valores en la tabla
2. **Agrega/Elimina** participantes con +/-
3. **Guarda** los cambios
4. **Distribuye** en equipos balanceados o aleatorios
5. **Comparte** el link con otros!
""")

st.sidebar.header("🌐 Compartir la App")
st.sidebar.write("""
Para hacer pública esta app:
1. Sube a Streamlit Cloud
2. Comparte el link generado
3. ¡Todos podrán usarla!
""")