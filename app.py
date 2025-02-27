import streamlit as st
import pandas as pd
import json

# Mengganti nama tab di browser
st.set_page_config(page_title="Voice Notes Counter")

def process_json(messages):
    leaderboard = pd.Series()

    for message in messages:
        # Periksa jika 'media_type' dan 'from' ada dalam pesan
        if 'media_type' in message and 'from' in message:
            # Filter hanya pesan yang bertipe 'voice_message'
            if message['media_type'] == 'voice_message':
                user = message['from']
                leaderboard = pd.concat([leaderboard, pd.Series([user])], ignore_index=True)

    return leaderboard

def style_leaderboard(user_count):
    # Styling untuk tabel leaderboard
    def color_negative_red(val):
        color = 'red' if val == user_count.max() else 'black'
        return f'color: {color}'

    styled_df = user_count.to_frame(name="Jumlah Pesan Suara").style.applymap(color_negative_red)
    return styled_df

def main():
    st.title("Leaderboard 1st Chapter VOTES INDONESIA")

    # Upload multiple files JSON
    uploaded_files = st.file_uploader("Upload File JSON", type=["json"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            leaderboard = pd.Series()

            try:
                # Membaca file yang diupload dan mengonversinya menjadi dictionary
                data = json.load(uploaded_file)

                # Pastikan data bukan None atau kosong
                if data is None or len(data) == 0:
                    st.error("Data JSON kosong atau tidak valid di file " + uploaded_file.name)
                    continue

                # Periksa apakah data memiliki key 'messages'
                if 'messages' not in data:
                    st.error(f"File {uploaded_file.name} tidak memiliki key 'messages'.")
                    continue

                # Proses data 'messages' untuk mendapatkan leaderboard
                leaderboard = process_json(data['messages'])

                # Hitung jumlah pesan suara per pengguna
                if not leaderboard.empty:
                    user_count = leaderboard.value_counts()
                    st.subheader(f"Leaderboard Pengirim Pesan Suara ({uploaded_file.name}):")
                    
                    # Menampilkan leaderboard dengan styling
                    styled_leaderboard = style_leaderboard(user_count)
                    st.dataframe(styled_leaderboard)

                else:
                    st.subheader(f"Leaderboard Pengirim Pesan Suara ({uploaded_file.name}):")
                    st.write("Tidak ada pesan suara ditemukan dalam file ini.")

            except json.JSONDecodeError:
                st.error(f"Gagal membaca file {uploaded_file.name}. Pastikan format file JSON sudah benar.")
            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses file {uploaded_file.name}: {e}")

if __name__ == "__main__":
    main()
