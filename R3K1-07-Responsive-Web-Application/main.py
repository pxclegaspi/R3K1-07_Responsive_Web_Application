import streamlit as st
from quiz_manager import QuizManager
#import cv2
#from IPython.display import YouTubeVideo
# import tkinter as tk
# from tkinter.ttk import *

# Page configuration
st.set_page_config(page_title="Physics Quiz App", page_icon="⚡", layout="wide")

# Load custom CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main():
    #Title - gets displayed no matter what
    # st.title("⚡ Physics Quiz")

    # Sidebar
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose which page to go to",
                                    ["Menu", "About", "Video: Review of the Laws", "Practice: Review of the Laws", "Video: Free-body Diagrams", "Practice: Free-body Diagrams", "Video: Gravitational Force, Projectile Motion", "Practice: Gravitational Force, Projectile Motion", "Video: Friction", "Practice: Friction"])
    # def changeChannel():
    #     global app_mode 
    #     app_mode = st.sidebar.selectbox("Choose the app mode",
    #         ["Menu", "Take Quiz", "About"], 
    #         index=2)

    quiz_manager = QuizManager()

    if app_mode == "Menu": #Self-explanatory
        st.write("## Welcome to the Newtonian Learning App!")
        st.write("""
        An app where you will learn Newton's Laws of Motion and their applications.
        """)
        st.write("### How to Use")
        st.write("""
        To access any video or practice, access the navigation bar, then choose which video or practice to go to by clicking the dropdown menu and the name of the video or practice you want to go to.
        """)
        # testing video
        # st.video('https://www.youtube.com/watch?v=4Ih36NzOSKA') 
        # st.video('videos/2024-11-24 14-14-46.mp4')
        #button test
        # app_mode = st.button(label="About", on_click=changeChannel())
        
    # elif app_mode == "Take Quiz":
    #     quiz_manager.display_question(0)

    elif app_mode == "Video: Review of the Laws":
        st.write("## Lesson 1: Review of the Laws")
        st.write("Objective:")
        st.write("- to review the three Laws of Motion by Newton")
        st.video('videos/lison wan edited video v1.mp4')

    elif app_mode == "Practice: Review of the Laws":
        quiz_manager.display_question(1)
    
    elif app_mode == "Video: Free-body Diagrams":
        st.write("## Lesson 2: Free-body Diagrams")
        st.write("Objective:")
        st.write("- to learn the basics of drawing free body diagrams")
        st.video('videos/lison to edited video v1.mp4')

    elif app_mode == "Practice: Free-body Diagrams":
        quiz_manager.display_question(2)

    elif app_mode == "Video: Gravitational Force, Projectile Motion":
        st.write("## Lesson 3: Gravitational Force, Projectile Motion")
        st.write("Objectives:")
        st.write("- to learn the basics of gravity and projectile motion")
        st.write("- to learn some basic formulas associated with gravity and projectile motion")
        st.video('videos/lison tri edited video v1.mp4')

    elif app_mode == "Practice: Gravitational Force, Projectile Motion":
        quiz_manager.display_question(3)

    elif app_mode == "Video: Friction":
        st.write("## Lesson 4: Friction")
        st.write("Objectives:")
        st.write("- to learn the basics of static and kinetic friction")
        st.write("- to learn some basic formulas associated with friction")
        st.video('videos/lison por edited video v1.mp4')

    elif app_mode == "Practice: Friction":
        quiz_manager.display_question(4)

    elif app_mode == "About":  # About
        st.write("## About the App")
        st.write("""
        This application aims to help you understand Newton's Laws of Motion and various examples related to it.
        Features include:
        - Short videos on the subject material
        - Practice questions, with instant feedback upon submitting answers 
        """)


if __name__ == "__main__":
    main()
