import streamlit as st
from gtts import gTTS
import numpy as np
import qrcode
from PIL import Image
from wordcloud import WordCloud ,STOPWORDS
import pywhatkit as kit
import webcolors as wb
from transformers import pipeline
import json
from streamlit_lottie import st_lottie
from link_button import link_button

st.set_page_config(page_title='Text converter',page_icon='👽')
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after {
	content:'Made with ❤️ by om pramod'; 
	visibility: visible ;
}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def home():
    st.markdown("<h1 style='text-align: center; color:black ;font-family: fantasy'>TEXT CONVERTER</h1>", unsafe_allow_html=True)
    st.markdown("****")
    st.success(" 👈 Select an option from sidebar menu")
    def load_lottiefile(filepath: str):
        with open(filepath, "r") as f :
            return json.load(f)

    lottie_coding = load_lottiefile("man.json")

    st_lottie(
        lottie_coding,
        speed= 1.5,
        reverse=False,
        loop=True,
        height=400,
        width= 700,
        key=None
    )

    link_button("🕸 Connect with me on linkedin","https://www.linkedin.com/in/omkar-h-7944a4202")


def speech():

    st.title("Text to speech converter")
    st.markdown("****")
    text = st.text_area("Enter your text here",height=200)

    english_accent = st.selectbox(
        "Select your english accent",
        (
            "Default",
            "India",
            "United Kingdom",
            "United States",
            "Canada",
            "Australia",
            "Ireland",
            "South Africa",
        ),
    )

    if english_accent == "Default":
        tld = "com"
    elif english_accent == "India":
        tld = "co.in"

    elif english_accent == "United Kingdom":
        tld = "co.uk"
    elif english_accent == "United States":
        tld = "com"
    elif english_accent == "Canada":
        tld = "ca"
    elif english_accent == "Australia":
        tld = "com.au"
    elif english_accent == "Ireland":
        tld = "ie"
    elif english_accent == "South Africa":
        tld = "co.za"

    if st.button("convert"):
        st.markdown("*****")
        with st.spinner("converting text to speech...."):
            try :
                tts = gTTS(text, lang='en', tld=tld, slow=False)
                tts.save("pyspeech.mp3")
                audio_file = open("pyspeech.mp3", "rb")
                audio_bytes = audio_file.read()
                st.markdown(f"## Your audio:")
                st.audio(audio_bytes, format="audio/mp3", start_time=0)
            except :
                st.error("kindly enter some text")

def hand() :
    st.title("Text to handwritting converter")
    st.markdown("****")
    text = st.text_area("enter your text here",height=340,help="paste your text here",max_chars=1040 )
    color = st.color_picker("choose font color",value="#1438E2")
    rgb = wb.hex_to_rgb(color)
    if st.button("convert"):
        st.markdown("****")
        with st.spinner("generating handwritten text"):
            try :
                img = kit.text_to_handwriting(text,save_to="gd.png",rgb=rgb)
                image_loaded = Image.open("gd.png")
                final = np.array(image_loaded)
                st.image(final)
                st.caption("right click on the image to download")
            except:
                st.error("Try again later")
        
def cloud():
    st.title("Word cloud generator")
    st.markdown("****")
    text = st.text_area("Enter your text here",height=200)

    background = st.selectbox("select the mask",[None,"bird","heart","cloud"])
    our_mask = None
    if background == "bird" :
        our_mask = np.array(Image.open("bird.jpeg"))
    elif background == "heart":
        our_mask = np.array(Image.open("heart.jpeg"))
    elif background == "cloud":
        our_mask = np.array(Image.open("cloud.jpeg"))

    if st.button("Generate") and text is not None:
        st.markdown("****")
        try:
            with st.spinner("generating word cloud"):
                wc = WordCloud(background_color = "white",mask=our_mask,stopwords=STOPWORDS,width=500,height=500)
                wc.generate(text)
                wc.to_file("wordcloud.png")
                st.image("wordcloud.png")
        except :
            st.error("kindly enter some text")

def QR():
    st.title("QR code generator" )
    st.markdown("****")
    text = st.text_area("Write ur text here",help="Kindly enter some text to generate QR code",height=200)
    version =st.slider("select version",1,30,step = 1)
    foreground = st.color_picker("Select foreground colour",value="#FFFFFF")
    background = st.color_picker("Select background colour")

    button = st.button("Generate QR code")
    if button and text is not None:
        st.markdown("****")
        with st.spinner("Generating QR code....") :
            try :
                qr = qrcode.QRCode(
                    version=version,
                    error_correction=qrcode.constants.ERROR_CORRECT_H,
                    box_size=40,
                    border=5
                )
                qr.add_data(text)
                qr.make(fit=True)             
                img = qr.make_image(fill_color=foreground, back_color=background)
                image = img.save("qrcode.png")
                image_loaded = Image.open("qrcode.png")
                final = np.array(image_loaded)
                st.image(final)
            except :
                st.error("Data Overflow Error - word limit exceeded")

def summary():
    @st.cache(allow_output_mutation=True)
    def load_summarizer():
        model = pipeline("summarization", device=0)
        return model

    summarizer = load_summarizer()

    st.title("Text summarizer")
    st.markdown("****")
    text = st.text_area("Enter your text here",height=200,help="paste the text to be summarized")
    if st.button("summarize") and text :
        st.markdown("****")
        with st.spinner("Generating Summary.."):
            summary = summarizer(text, max_length=100, min_length=10, do_sample=False)
            st.write(summary[0]["summary_text"])

sidebar = st.sidebar.selectbox("Menu",["Home","Text to speech converter","Test to handwritting converter","Word cloud generator","QR code generator","Text summarizer"])

if sidebar== "Home":
    home()
elif sidebar== "Text to speech converter" :
    speech()
elif sidebar== "Test to handwritting converter" :
    hand()
elif sidebar== "Word cloud generator":
    cloud()
elif sidebar== "QR code generator" :
    QR()
elif sidebar == "Text summarizer" :
    summary()