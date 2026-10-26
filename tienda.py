import streamlit as st
import pandas as pd

st.set_page_config(page_title="Boutique Inteligente", page_icon="👗", layout="wide")

# ─── BASE DE DATOS SIMULADA ───
if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame([
        {"id": 1, "producto": "Camisa Oversize", "precio": 25.0, "costo": 10.0, "stock": 15, "vendidos": 5, "img": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400"},
        {"id": 2, "producto": "Pantalón Cargo", "precio": 35.0, "costo": 18.0, "stock": 8, "vendidos": 2, "img": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=400"},
        {"id": 3, "producto": "Vestido Floral", "precio": 45.0, "costo": 15.0, "stock": 20, "vendidos": 15, "img": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=400"}
    ])

df = st.session_state.inventario

# ─── INTERFAZ PRINCIPAL ───
st.title("👗 Boutique Inteligente")
st.markdown("Bienvenido. Por favor selecciona tu perfil.")
st.markdown("---")

# Creamos dos opciones en la barra lateral para separar Cliente y Dueño
rol = st.sidebar.radio("Ingresa como:", ["🛍️ Cliente", "🔐 Dueño (Administrador)"])

# ═══════════════════════════════════════════════════════════
# VISTA DEL CLIENTE
# ═══════════════════════════════════════════════════════════
if rol == "🛍️ Cliente":
    st.header("Catálogo de Temporada")
    
    cols = st.columns(2)
    for index, row in df.iterrows():
        with cols[index % 2]:
            st.image(row["img"], use_column_width=True)
            st.markdown(f"**{row['producto']}**")
            st.markdown(f"💵 Precio: **${row['precio']}**")
            
            if row["stock"] > 0:
                if st.button(f"🛒 Comprar", key=f"btn_{row['id']}"):
                    st.session_state.inventario.loc[index, 'stock'] -= 1
                    st.session_state.inventario.loc[index, 'vendidos'] += 1
                    st.success(f"¡Compraste {row['producto']}!")
                    st.rerun()
            else:
                st.error("❌ Agotado")

# ═══════════════════════════════════════════════════════════
# VISTA DEL DUEÑO (PROTEGIDA CON CONTRASEÑA)
# ═══════════════════════════════════════════════════════════
else:
    # Contraseña secreta para entrar
    password = st.text_input("Ingresa la clave de administrador:", type="password")
    
    if password == "admin123": # Puedes cambiar esta clave aquí
        st.success("Acceso concedido. Bienvenido, Dueño.")
        
        # --- FORMULARIO PARA SUBIR MERCANCÍA NUEVA ---
        with st.expander("📦 Ingresar Mercancía Nueva (Haz clic aquí)"):
            with st.form("nuevo_producto"):
                st.markdown("Llena los datos de la prenda que acaba de llegar:")
                col1, col2 = st.columns(2)
                with col1:
                    nuevo_nombre = st.text_input("Nombre de la prenda")
                    nuevo_costo = st.number_input("Costo ($)", min_value=1.0)
                with col2:
                    nueva_cantidad = st.number_input("Cantidad que llegó", min_value=1)
                    nuevo_precio = st.number_input("Precio de venta ($)", min_value=1.0)
                
                # Imagen por defecto si no se sube una
                nueva_img = st.text_input("URL de la foto (Opcional)", value="https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=400")
                
                submit_btn = st.form_submit_button("Guardar en Inventario")
                
                if submit_btn and nuevo_nombre:
                    # Crear nueva fila
                    nuevo_id = st.session_state.inventario['id'].max() + 1
                    nueva_fila = pd.DataFrame([{
                        "id": nuevo_id, "producto": nuevo_nombre, "precio": nuevo_precio, 
                        "costo": nuevo_costo, "stock": nueva_cantidad, "vendidos": 0, "img": nueva_img
                    }])
                    # Agregar a la base de datos
                    st.session_state.inventario = pd.concat([st.session_state.inventario, nueva_fila], ignore_index=True)
                    st.success("¡Mercancía agregada con éxito!")
                    st.rerun()

        # --- ANÁLISIS PREDICTIVO ---
        st.markdown("### 📊 Análisis Financiero (Sofi Pro)")
        df = st.session_state.inventario
        df["ganancia_unitaria"] = df["precio"] - df["costo"]
        total_ganancia = (df["ganancia_unitaria"] * df["vendidos"]).sum()
        
        st.metric("Ganancia Neta Total", f"${total_ganancia:,.2f}")
        
        st.markdown("#### 🚨 Alertas de la IA")
        for index, row in df.iterrows():
            if row["stock"] <= 3:
                st.error(f"⚠️ **Poco Stock:** Solo quedan {row['stock']} de **{row['producto']}**.")
            margen = (row["ganancia_unitaria"] / row["precio"]) * 100
            if margen < 30:
                st.warning(f"📉 **Margen Bajo:** **{row['producto']}** te deja solo {margen:.1f}%. Súbele el precio.")
                
    elif password != "":
        st.error("Contraseña incorrecta. Acceso denegado.")