import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
from database import Database
from utils import format_time

# Static questions list
QUESTIONS_ZERO = [
    {
        'id': 1,
        'question_text': 'What is the acceleration due to gravity on Earth?',
        'options': ['9.81 m/s²', '8.91 m/s²', '10.1 m/s²', '7.91 m/s²'],
        'correct_answer': '9.81 m/s²',
        'formula': r'g = 9.81\,\text{m}/\text{s}^2'
    },
    {
        'id': 2,
        'question_text': 'Which formula represents kinetic energy?',
        'options': ['KE = ½mv²', 'KE = mgh', 'KE = mv', 'KE = m/v'],
        'correct_answer': 'KE = ½mv²',
        'formula': r'KE = \frac{1}{2}mv^2'
    },
    {
        'id': 3,
        'question_text': "What is Newton's second law of motion?",
        'options': ['F = ma', 'F = mv', 'F = m/a', 'F = m²a'],
        'correct_answer': 'F = ma',
        'formula': r'F = ma'
    }
]
QUESTIONS_ONE = [
    {
        'id': 1,
        'question_text': 'On a flat frictionless surface, Mark sits down and pushes himself forward. What will happen to him?',
        'options': ['He will eventually come to a stop.', 'He will keep on going at a constant pace.', 'He will go faster and faster.'],
        'correct_answer': 'He will keep on going at a constant pace.',
        'formula': None
    },
    {
        'id': 2,
        'question_text': 'On Earth, a ball is dropped from a certain height. Which of the two is exerting more force?',
        'options': ['Earth', 'the ball', 'They are both exerting equal force.'],
        'correct_answer': 'They are both exerting equal force.',
        'formula': None
    },
    {
        'id': 3,
        'question_text': "If a person walking suddenly stops, is there a net force on them?",
        'options': ['Yes, because there is a change in velocity, and hence acceleration.', 'No, because no object was exerting force on the person.', 'Yes, because of the friction on the surface they are walking on.'],
        'correct_answer': 'Yes, because there is a change in velocity, and hence acceleration.',
        'formula': None
    },
    {
        'id': 4,
        'question_text': "Peter pushes down on a table through some dough he is kneading. If the table were a person, what would be the best description of the action of the table here, using Newton's Laws of Motion?",
        'options': ['They are resisting the pushing of Peter.', 'They are helping knead the dough.', 'They are pushing up on Peter.'],
        'correct_answer': 'They are resisting the pushing of Peter.',
        'formula': None
    }
]
QUESTIONS_TWO = [
    {
        'id': 1,
        'question_text': 'Ashley is standing still. What will be the free-body diagram for her?',
        'options': ['No arrows', 'Arrow pointing down for gravity, arrow pointing up for normal force', 'Arrow pointing down for gravity'],
        'correct_answer': 'Arrow pointing down for gravity, arrow pointing up for normal force',
        'formula': None
    },
    {
        'id': 2,
        'question_text': 'A box was being pushed to the right. A free-body diagram was made for it, with an arrow pointing right for the pushing force and an arrow pointing left for the friction. What is missing in the FBD?',
        'options': ['Arrow pointing down for the gravitational force', 'Arrow pointing up for the normal force', 'All of the above'],
        'correct_answer': 'All of the above',
        'formula': None
    },
    {
        'id': 3,
        'question_text': "Jana hung a picture frame on her wall. The string where the picture frame hangs from has one point of contact on the back. What will be the FBD of the picture frame?",
        'options': ['Arrow pointing up for tension, Arrow pointing down for gravity', 'Arrow pointing up for tension', 'No arrows'],
        'correct_answer': 'Arrow pointing up for tension, Arrow pointing down for gravity',
        'formula': None
    },
    {
        'id': 4,
        'question_text': "A hockey puck was sliding across the ice rink after a hockey player hit it to pass to their teammate. Carlo, while watching, saw the puck go to the left and attempted to draw a free-body diagram of the puck. His FBD had an arrow pointing left for the force of the pass, an arrow pointing right for the friction of the ice, an arrow pointing up for the normal force, and an arrow pointing down for the gravitational force. Was his FBD valid?",
        'options': ['Yes, all forces were accounted for.', 'No, the arrow for the force of the pass was not needed.', 'No, the arrow for the friction was not needed.'],
        'correct_answer': 'No, the arrow for the force of the pass was not needed.',
        'formula': None
    }
]
QUESTIONS_THREE = [
    {
        'id': 1,
        'question_text': 'Raindrops usually fall from a height of about 2.00 km above ground. How long will it take to reach the ground?',
        'options': None,
        'correct_answer': '20.2 s',
        'formula': None
    },
    {
        'id': 2,
        'question_text': 'Alex, an astronaut, is exploring an exoplanet with an unknown gravity. They dropped a hammer 1.50 m above ground. If the hammer takes about 0.775 s to fall to the ground, what is the gravity of the exoplanet?',
        'options': None,
        'correct_answer': '5.00 m/s^2',
        'formula': None
    },
    {
        'id': 3,
        'question_text': "A trebuchet launches a piece of Potchi at an initial speed of 3.14 m/s and at an angle of θ = 45.0°. How long will it take before the Potchi lands?",
        'options': None,
        'correct_answer': '0.453 s',
        'formula': None
    },
    {
        'id': 4,
        'question_text': "AJ is practicing archery. They shot an arrow straight on at a wall 10.0 m away with an initial speed of 40.0 m/s. By how much will the arrow fall due to gravity before it reaches the wall?",
        'options': None,
        'correct_answer': '0.307 m',
        'formula': None
    }
]
QUESTIONS_FOUR = [
    {
        'id': 1,
        'question_text': "Craig was pushing a heavy box weighing 40.0 kg. He exerted 500. N of force at it, yet it still wasn't moving. What is the minimum coefficient of static friction of the ground to the box?",
        'options': None,
        'correct_answer': '0.785',
        'formula': None
    },
    {
        'id': 2,
        'question_text': 'A hockey puck, with a mass of 0.170 kg, was being guided by a hockey stick with a force of 1.00 N. The ice rink has a coefficient of kinetic friction to the hockey puck of 0.100. What is the acceleration of the hockey puck?',
        'options': None,
        'correct_answer': '4.90 m/s^2',
        'formula': None
    },
    {
        'id': 3,
        'question_text': 'A very rough surface has a coefficient of static friction to most materials of 0.900. At least how much force is needed to push a 75.0 kg box along this surface?',
        'options': None,
        'correct_answer': '662 N',
        'formula': None
    },
    {
        'id': 4,
        'question_text': "A table has a coefficient of kinetic friction to most materials of 0.450. How much force will be needed to maintain a constant speed of 1.00 m/s for an object with a mass of 0.100 kg?",
        'options': None,
        'correct_answer': '0.441 N',
        'formula': None
    }
]

class QuizManager:
    def __init__(self):
        self.db = Database()
        
        # Initialize session state variables
        if 'current_question' not in st.session_state:
            st.session_state.current_question = 0
        if 'show_answer' not in st.session_state:
            st.session_state.show_answer = False
        if 'start_time' not in st.session_state:
            st.session_state.start_time = time.time()
        if 'username' not in st.session_state:
            st.session_state.username = None
        if 'user_id' not in st.session_state:
            st.session_state.user_id = None

    def login(self):
        #checks if user is logged in
        if not st.session_state.username:
            username = st.text_input("Enter your username to track progress:")
            #checks if may nakalagay na sa username box
            if username:
                st.session_state.username = username
                st.session_state.user_id = self.db.get_or_create_user(username)
                st.rerun()

    def display_statistics(self):
        #checks if may stats na yung user; stats are saved on refresh and even on exit and reentry
        if st.session_state.user_id:
            stats = self.db.get_user_statistics(st.session_state.user_id)
            if stats:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Attempts", stats['total_attempts'])
                with col2:
                    accuracy = (stats['correct_answers'] / stats['total_attempts'] * 100) if stats['total_attempts'] > 0 else 0
                    st.metric("Accuracy", f"{accuracy:.1f}%")
                with col3:
                    avg_time = stats['total_time'] / stats['total_attempts'] if stats['total_attempts'] > 0 else 0
                    st.metric("Avg. Time per Question", format_time(avg_time))

    def display_question(self, lessonNumber):
        self.login()
        
        if not st.session_state.username:
            return

        self.display_statistics()
        if lessonNumber == 0:
            if st.session_state.current_question >= len(QUESTIONS_ZERO):
                if st.button("Start New Quiz"):
                    st.session_state.current_question = 0
                    st.session_state.start_time = time.time()
                    st.rerun()
                return

            question = QUESTIONS_ZERO[st.session_state.current_question]

            st.write(f"Question {st.session_state.current_question + 1} of {len(QUESTIONS_ZERO)}")
            st.markdown(f"### {question['question_text']}")

            if question['formula']:
                st.latex(question['formula'])

            # Add toggle for showing/hiding answer
            show_answer = st.checkbox("Show Answer", key=f"show_answer_{st.session_state.current_question}")
            if show_answer:
                st.info(f"Correct answer: {question['correct_answer']}")

            if question['options']:
                choice = st.radio("Select your answer:", question['options'], key=f"q_{st.session_state.current_question}")
            

            if st.button("Submit Answer"):
                time_taken = int(time.time() - st.session_state.start_time)
                is_correct = choice == question['correct_answer']

                # Record the attempt
                self.db.record_attempt(
                    st.session_state.user_id,
                    question['id'],
                    is_correct,
                    time_taken
                )

                # Show result
                if is_correct:
                    st.success("Correct! 🎉")
                else:
                    st.error("Incorrect. Try again! 💪")

                # Reset timer and move to next question
                st.session_state.start_time = time.time()
                st.session_state.current_question += 1
                st.rerun()
        elif lessonNumber == 1:
            if st.session_state.current_question >= len(QUESTIONS_ONE):
                if st.button("Start New Quiz"):
                    st.session_state.current_question = 0
                    st.session_state.start_time = time.time()
                    st.rerun()
                return

            question = QUESTIONS_ONE[st.session_state.current_question]

            st.write(f"Question {st.session_state.current_question + 1} of {len(QUESTIONS_ONE)}")
            st.markdown(f"### {question['question_text']}")

            if question['formula']:
                st.latex(question['formula'])

            # Add toggle for showing/hiding answer
            show_answer = st.checkbox("Show Answer", key=f"show_answer_{st.session_state.current_question}")
            if show_answer:
                st.info(f"Correct answer: {question['correct_answer']}")

            if question['options']:
                choice = st.radio("Select your answer:", question['options'], key=f"q_{st.session_state.current_question}")


            if st.button("Submit Answer"):
                time_taken = int(time.time() - st.session_state.start_time)
                is_correct = choice == question['correct_answer']

                # Record the attempt
                self.db.record_attempt(
                    st.session_state.user_id,
                    question['id'],
                    is_correct,
                    time_taken
                )

                # Show result
                if is_correct:
                    st.success("Correct! 🎉")
                else:
                    st.error("Incorrect. Try again! 💪")

                # Reset timer and move to next question
                st.session_state.start_time = time.time()
                st.session_state.current_question += 1
                st.rerun()
        elif lessonNumber == 2:
            if st.session_state.current_question >= len(QUESTIONS_TWO):
                if st.button("Start New Quiz"):
                    st.session_state.current_question = 0
                    st.session_state.start_time = time.time()
                    st.rerun()
                return
        
            question = QUESTIONS_TWO[st.session_state.current_question]
        
            st.write(f"Question {st.session_state.current_question + 1} of {len(QUESTIONS_TWO)}")
            st.markdown(f"### {question['question_text']}")
        
            if question['formula']:
                st.latex(question['formula'])
        
            # Add toggle for showing/hiding answer
            show_answer = st.checkbox("Show Answer", key=f"show_answer_{st.session_state.current_question}")
            if show_answer:
                st.info(f"Correct answer: {question['correct_answer']}")
        
            if question['options']:
                choice = st.radio("Select your answer:", question['options'], key=f"q_{st.session_state.current_question}")
        
        
            if st.button("Submit Answer"):
                time_taken = int(time.time() - st.session_state.start_time)
                is_correct = choice == question['correct_answer']
        
                # Record the attempt
                self.db.record_attempt(
                    st.session_state.user_id,
                    question['id'],
                    is_correct,
                    time_taken
                )
        
                # Show result
                if is_correct:
                    st.success("Correct! 🎉")
                else:
                    st.error("Incorrect. Try again! 💪")
        
                # Reset timer and move to next question
                st.session_state.start_time = time.time()
                st.session_state.current_question += 1
                st.rerun()
        elif lessonNumber == 3:
            if st.session_state.current_question >= len(QUESTIONS_THREE):
                if st.button("Start New Quiz"):
                    st.session_state.current_question = 0
                    st.session_state.start_time = time.time()
                    st.rerun()
                return

            question = QUESTIONS_THREE[st.session_state.current_question]

            st.write(f"Question {st.session_state.current_question + 1} of {len(QUESTIONS_THREE)}")
            st.markdown(f"### {question['question_text']}")

            # if question['formula']:
            #     st.latex(question['formula'])

            # Add toggle for showing/hiding answer
            show_answer = st.checkbox("Show Answer", key=f"show_answer_{st.session_state.current_question}")
            if show_answer:
                st.info(f"Correct answer: {question['correct_answer']}")

            choice = st.text_input("Enter your answer here:")

            if st.button("Submit Answer"):
                time_taken = int(time.time() - st.session_state.start_time)
                is_correct = choice == question['correct_answer']

                # Record the attempt
                self.db.record_attempt(
                    st.session_state.user_id,
                    question['id'],
                    is_correct,
                    time_taken
                )

                # Show result
                if is_correct:
                    st.success("Correct! 🎉")
                else:
                    st.error("Incorrect. Try again! 💪")

                # Reset timer and move to next question
                st.session_state.start_time = time.time()
                st.session_state.current_question += 1
                st.rerun()
        elif lessonNumber == 4:
            if st.session_state.current_question >= len(QUESTIONS_FOUR):
                if st.button("Start New Quiz"):
                    st.session_state.current_question = 0
                    st.session_state.start_time = time.time()
                    st.rerun()
                return
    
            question = QUESTIONS_FOUR[st.session_state.current_question]
    
            st.write(f"Question {st.session_state.current_question + 1} of {len(QUESTIONS_FOUR)}")
            st.markdown(f"### {question['question_text']}")
    
            # if question['formula']:
            #     st.latex(question['formula'])
    
            # Add toggle for showing/hiding answer
            show_answer = st.checkbox("Show Answer", key=f"show_answer_{st.session_state.current_question}")
            if show_answer:
                st.info(f"Correct answer: {question['correct_answer']}")
    
            choice = st.text_input("Enter your answer here:")
    
            if st.button("Submit Answer"):
                time_taken = int(time.time() - st.session_state.start_time)
                is_correct = choice == question['correct_answer']
    
                # Record the attempt
                self.db.record_attempt(
                    st.session_state.user_id,
                    question['id'],
                    is_correct,
                    time_taken
                )
    
                # Show result
                if is_correct:
                    st.success("Correct! 🎉")
                else:
                    st.error("Incorrect. Try again! 💪")
    
                # Reset timer and move to next question
                st.session_state.start_time = time.time()
                st.session_state.current_question += 1
                st.rerun()