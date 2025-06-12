import streamlit as st
import json

from profiles import create_profile, get_profile, get_notes, delete_profile
from form_submit import update_personal_data, add_note, delete_note 
from ai import ask_ai, calculate_macros

# -------------------------------
# Streamlit App Title
# -------------------------------
st.title("Workout Helper App")  # Set the app title

# -------------------------------
# Personal Data Form
# -------------------------------
@st.fragment()
def personal_data_form():
    """
    Renders a form for editing personal data (name, age, weight, height, gender, activity level).
    Updates session state on submit.
    """
    with st.form("personal_data"):
        # Retrieve profile and notes from session state
        profile = st.session_state.profile
        notes = st.session_state.notes

        st.header("Personal Data")
        # Input fields for personal data
        name = st.text_input("Name", value=profile['general']['name'])
        age = st.number_input("Age", value=profile['general']['age'], min_value=1, max_value=120, step=1)
        weight = st.number_input("Weight (kg)", min_value=0.0, max_value=500.0, step=0.1, value=float(profile['general']['weight']))
        height = st.number_input("Height (cm)", min_value=0.0, max_value=300.0, step=0.1, value=float(profile['general']['height']))

        # Gender selection
        genders = ['Male', 'Female', 'Other']
        gender = st.radio('Gender', genders, genders.index(profile['general'].get('gender', 'Male'))) 

        # Activity level selection
        activity_levels = ['Sedentary', 'Lightly Active', 'Moderately Active', 'Very Active', 'Super Active']
        activity_level = st.selectbox(
            'Activity Level',
            activity_levels, 
            index=activity_levels.index(profile['general'].get('activity_level', 'Moderately Active'))
        )
                                     
        submit_button = st.form_submit_button("Save")
        if submit_button:
            # Validate all fields are filled
            if all([name, age, weight, height, gender, activity_level]):
                with st.spinner("Saving..."):
                    # Save updated personal data to session state
                    st.session_state.profile = update_personal_data(
                        profile,
                        'general',
                        name=name,
                        age=age,
                        weight=weight,
                        height=height,
                        gender=gender,
                        activity_level=activity_level
                    )
                    st.success("Personal data saved!")
            else:
                st.error("Please fill in all fields.")

# -------------------------------
# Goals Form
# -------------------------------
@st.fragment()
def goals_form():
    """
    Renders a form for selecting fitness goals.
    Updates session state on submit.
    """
    profile = st.session_state.profile
    with st.form("Goals Form"):
        st.header('Goals')
        # Multiselect for fitness goals
        goals = st.multiselect(
            'Select your goals', 
            ['Muscle Gain', 'Fat Loss', 'Stay Active'], 
            default=profile.get('goals', ['Stay Active']),
        )

        goals_submit = st.form_submit_button("Save")
        if goals_submit:
            if goals:
                with st.spinner("Saving..."):
                    # Save updated goals to session state
                    st.session_state.profile = update_personal_data(profile, 'goals', goals=goals)
                    st.success("Goals saved!")
            else:
                st.warning("Please select at least one goal.")

# -------------------------------
# Macros Form
# -------------------------------
@st.fragment()
def macros():
    """
    Renders a section for generating and editing nutrition macros.
    Allows AI-based macro calculation and manual editing.
    """
    profile = st.session_state.profile
    nutrition = st.container(border=True)
    nutrition.header("Macros")
    # Button to generate macros using AI
    if nutrition.button("Generate Macros With AI"):
        with st.spinner("Generating macros..."):
            # Call the AI function to calculate macros
            result = json.loads(calculate_macros(profile['goals'], profile['general']))
            profile['nutrition'] = result
            nutrition.success("Macros generated!")

    # Form for manual macro editing
    with nutrition.form('nutrition_form', border=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            calories = st.number_input("Calories", min_value=0, step=1, value=int(profile['nutrition'].get('calories', 0)))
        with col2:
            protein = st.number_input("Protein (g)", min_value=0, step=1, value=int(profile['nutrition'].get('protein', 0)))
        with col3:
            carbs = st.number_input("Carbs (g)", min_value=0, step=1, value=int(profile['nutrition'].get('carbs', 0)))
        with col4:
            fats = st.number_input("Fats (g)", min_value=0, step=1, value=int(profile['nutrition'].get('fats', 0)))
            
        # Save button for macros
        if st.form_submit_button("Save"):
            if all([calories, protein, carbs, fats]):
                with st.spinner("Saving..."):
                    # Save updated nutrition data to session state
                    st.session_state.profile = update_personal_data(
                        profile,
                        'nutrition',
                        calories=calories,
                        protein=protein,
                        carbs=carbs,
                        fats=fats
                    )
                    st.success("Nutrition data saved!")
            else:
                st.error("Please fill in all fields.")

# -------------------------------
# Notes Form
# -------------------------------
@st.fragment()
def notes_form():
    """
    Renders a section for displaying, adding, and deleting notes.
    Notes are stored in session state.
    """
    st.subheader("Notes: ")
    # Display existing notes with delete buttons
    for i, note in enumerate(st.session_state.notes):
        cols = st.columns([5, 1])
        with cols[0]:
            st.text(note.get('text', ''))
        with cols[1]:
            if st.button("Delete", key=f"delete_{i}"):
                with st.spinner("Deleting..."):
                    delete_note(note['_id'])
                    st.session_state.notes.pop(i)
                    st.rerun()

    # Input for adding a new note
    new_note = st.text_input("Add a note")
    if st.button("Add Note"):
        if new_note:
            with st.spinner("Adding note..."):
                # Add new note to session state
                note = add_note(new_note, st.session_state.profile_id)
                st.session_state.notes.append(note)
                st.success("Note added!")
                st.rerun()
        else:
            st.error("Please enter a note.")

# -------------------------------
# Ask AI Form
# -------------------------------
@st.fragment()
def ask_ai_func():
    """
    Renders a section for asking questions to the AI.
    Displays the AI's response.
    """
    st.subheader("Ask AI: ")
    question = st.text_input("Ask a question: ")
    if st.button("Ask AI"):
        with st.spinner("Asking AI..."):
            # Call the AI function to get a response
            result = ask_ai(question, st.session_state.profile)
            st.write(result)

# -------------------------------
# Main Forms Handler
# -------------------------------
def forms():
    """
    Initializes session state for profile and notes if not present.
    Renders the personal data, goals, macros, notes, and AI forms.
    """
    # Initialize profile in session state if not present
    if 'profile' not in st.session_state:
        profile_id = 1  # Default profile ID
        new_profile_id, profile = get_profile(profile_id)
    
        if not profile: 
            new_profile_id, profile = create_profile(profile_id)
        st.session_state.profile = profile
        st.session_state.profile_id = new_profile_id

    # Initialize notes in session state if not present
    if 'notes' not in st.session_state:
        notes = get_notes(st.session_state.profile_id)
        st.session_state.notes = notes

    # Render all forms
    personal_data_form()
    goals_form()
    macros()
    notes_form()
    ask_ai_func()

# -------------------------------
# App Entry Point
# -------------------------------
if __name__ == "__main__":
    # Run the main forms handler to start the app
    forms()