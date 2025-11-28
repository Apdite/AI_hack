import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from models.video_tracker import analyze_video

st.title("Умный анализ видео: Детекция и трекинг людей на заводе")

# Загрузка видео
uploaded = st.file_uploader("Загрузите видео (mp4 с Yandex или любое)", type="mp4")
if uploaded:
    with open("temp.mp4", "wb") as f: f.write(uploaded.read())
    if st.button("Анализировать видео"):
        with st.spinner("Обработка... (может занять 1-2 мин на длинном видео)"):
            df = analyze_video("temp.mp4")
        st.success(f"Обнаружено {df['id'].nunique()} уникальных людей! ID сохраняются при повторном появлении.")

        # Wow: Timeline динамики ID
        st.subheader("Timeline: Когда люди появлялись (по ID)")
        fig, ax = plt.subplots(figsize=(10, 5))
        for person_id in df['id'].unique():
            person_df = df[df['id'] == person_id]
            ax.plot(person_df['frame'], [person_id] * len(person_df), marker='o', label=f'ID {person_id}')
        ax.set_xlabel('Кадр (время)')
        ax.set_ylabel('ID человека')
        ax.legend()
        st.pyplot(fig)

        # Wow: Heatmap позиций (где люди чаще)
        st.subheader("Heatmap: Горячие зоны людей (bbox центры)")
        if not df.empty:
            positions = pd.DataFrame([{'x': (b[0] + b[2])/2, 'y': (b[1] + b[3])/2} for b in df['bbox']])
            fig2, ax2 = plt.subplots(figsize=(8, 6))
            sns.kdeplot(data=positions, x='x', y='y', cmap='Reds', fill=True, ax=ax2)
            ax2.invert_yaxis()  # Корректные координаты видео
            ax2.set_title("Распределение позиций людей")
            st.pyplot(fig2)
        else:
            st.info("Нет данных для heatmap.")

        # Таблица логов для отладки
        st.subheader("Логи (CSV-вывод)")
        st.dataframe(df)