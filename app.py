import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Сфиральная квантовая система")
uploaded_file = st.file_uploader("Загрузите JSON с данными измерений", type="json")

if uploaded_file:
    try:
        df = pd.read_json(uploaded_file)
        top_n = 10
        df_counts = df["statevector"].value_counts().reset_index()
        df_counts.columns = ["Состояние", "Частота"]
        df_top = df_counts.head(top_n)

        fig, ax = plt.subplots(figsize=(10, 4))
        sns.barplot(x="Состояние", y="Частота", data=df_top, palette="Blues_r", ax=ax)
        ax.set_title(f"Частота появления топ-{top_n} состояний")
        ax.set_xlabel("Состояние")
        ax.set_ylabel("Частота")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        st.success("Данные успешно загружены и обработаны!")

    except Exception as e:
        st.error(f"Ошибка при обработке файла: {e}")
