import streamlit as st
import pandas as pd

st.set_page_config(page_title="Boutique Inteligente", page_icon="👗", layout="wide")

# ─── BASE DE DATOS SIMULADA (Aquí conectarías Sofi Pro real) ───
if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame([
        {"id": 1, "producto": "Camisa Oversize", "categoria": "Camisas", "precio": 25.0, "costo": 10.0, "stock": 15, "vendidos": 5, "img": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400"},
        {"id": 2, "producto": "Pantalón Cargo", "categoria": "Pantalones", "precio": 35.0, "costo": 18.0, "stock": 8, "vendidos": 2, "img": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=400"},
        {"id": 3, "producto": "Vestido Floral", "categoria": "Vestidos", "precio": 45.0, "costo": 15.0, "stock": 20, "vendidos": 15, "img": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=400"},
        {"id": 4, "producto": "Chaqueta Denim", "categoria": "Chaquetas", "precio": 60.0, "costo": 35.0, "stock": 3, "vendidos": 18, "img": "https://images.unsplash.com/photo-1527010152798-8971d2e0881b?w=400"}
    ])

df = st.session_state.inventario

# ─── INTERFAZ PRINCIPAL ───
st.title("👗 Boutique Inteligente")
st.markdown("Bienvenido a la tienda que no solo vende ropa, sino que **sabe qué comprar**.")
st.markdown("---")

tab_tienda, tab_admin = st.tabs(["🛍️ Ver Tienda", "🧠 Panel Inteligente (Dueño)"])

# ─── PESTAÑA 1: TIENDA ───
with tab_tienda:
    st.markdown("### Catálogo de Temporada")
    
    # Creamos columnas para mostrar los productos
    cols = st.columns(2)
    for index, row in df.iterrows():
        with cols[index % 2]:
            st.image(row["img"], use_column_width=True)
            st.markdown(f"**{row['producto']}**")
            st.markdown(f"💵 Precio: **${row['precio']}**")
            
            if row["stock"] > 0:
                if st.button(f"🛒 Comprar {row['producto']}", key=f"btn_{row['id']}"):
                    # Lógica de compra (restar stock y sumar ventas)
                    st.session_state.inventario.loc[index, 'stock'] -= 1
                    st.session_state.inventario.loc[index, 'vendidos'] += 1
                    st.success(f"¡Compraste {row['producto']}!")
                    st.rerun()
            else:
                st.error("❌ Agotado")

# ─── PESTAÑA 2: EL "CEREBRO" (Panel Sofi Pro) ───
with tab_admin:
    st.markdown("### 📊 Análisis Predictivo del Negocio")
    st.info("Esta sección analiza la tienda en tiempo real para ayudarte a ganar más dinero.")
    
    # 1. Cálculo de Ganancias
    df["ganancia_unitaria"] = df["precio"] - df["costo"]
    df["ganancia_total"] = df["ganancia_unitaria"] * df["vendidos"]
    total_ingresos = (df["precio"] * df["vendidos"]).sum()
    total_ganancia = df["ganancia_total"].sum()
    
    col_m1, col_m2 = st.columns(2)
    col_m1.metric("Ingresos Totales", f"${total_ingresos:,.2f}")
    col_m2.metric("Ganancia Neta", f"${total_ganancia:,.2f}")
    
    st.markdown("---")
    st.markdown("#### 🚨 Alertas de Sofi Pro (IA)")
    
    for index, row in df.iterrows():
        # Alerta 1: Poco Stock
        if row["stock"] <= 3:
            st.error(f"⚠️ **¡Alerta de Stock!** Solo te quedan **{row['stock']}** unidades de **{row['producto']}**. Basado en tus ventas, se agotará pronto. Pide más al proveedor.")
            
        # Alerta 2: Bajo Margen
        margen = (row["ganancia_unitaria"] / row["precio"]) * 100
        if margen < 30:
            st.warning(f"📉 **Margen Bajo:** **{row['producto']}** solo te deja un {margen:.1f}% de ganancia. Te sugiero subirle el precio a **${row['costo'] * 1.5:.2f}**.")

    st.markdown("---")
    st.markdown("#### 🏆 Productos Más Vendidos")
    top_ventas = df.sort_values(by="vendidos", ascending=False)[["producto", "vendidos"]]
    st.dataframe(top_ventas, hide_index=True, use_container_width=True)
  
