import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

model_fraud = pickle.load(open('model_deteksi_komentar.sav','rb'))

tfidf = TfidfVectorizer

loaded_vec = TfidfVectorizer(decode_error="replace", vocabulary=set(pickle.load(open("new_selected_feature_tf-idf.sav", "rb"))))


def send_email(sender_email, sender_password, receiver_email, subject, message):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    with smtplib.SMTP("smtp-mail.outlook.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

def main():
    st.title("Kritik Dan Saran Untuk Rismajt")

    sender_email = st.text_input("Masukan Emailmu")
    sender_password = st.text_input("Password", type="password")
    receiver_email = "jojogorakso@gmail.com"
    subject = st.text_input("Judul Artikel yang ingin diberi masukan")
    message = st.text_area("Masukan")

    st.write("<style>.stButton>button {width: 100%;}</style>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    if col1.button("Kirim Masukan"):
        send_email(sender_email, sender_password, receiver_email, subject, message)
        st.success("Email sent successfully!")

    if col2.button("Deteksi Sentimen Masukan"):
        predict_fraud = model_fraud.predict(loaded_vec.fit_transform([message]))
    
        if (predict_fraud == 0):
            fraud_detection = 'Masukan kamu terindikasi hatespeech'
        elif (predict_fraud == 1):
            fraud_detection = 'Terima kasih masukannya, sangat membangun'
        else :
            fraud_detection = 'inputanmu salah'
        st.success(fraud_detection)

if __name__ == "__main__":
    main()
