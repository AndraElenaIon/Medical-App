import streamlit as st
from MedicalDiagnosisApplication import get_diagnosis, get_diseases_by_medication, get_doctors_by_specialty, diseases, doctors, patients

# Construiți interfața cu Streamlit
st.title("Sistem de Interogare a Bazei de Cunoștințe Medicale")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Diagnosticare", "Istoric Medical", "Informații Pacient", "Informații Doctor", "Boli și Medicamente"])

with tab1:
    with tab1:
        st.subheader("Diagnosticare pe baza simptomelor")
        selected_symptoms = st.multiselect("Selectați simptomele:",
                                           list(set(sum([d['symptoms'] for d in diseases.values()], []))))
        if st.button("Obțineți Diagnosticul"):
            certain_diagnosis, possible_diagnoses = get_diagnosis(selected_symptoms)

            if certain_diagnosis:
                st.success(f"Diagnostic sigur: {certain_diagnosis}")
            else:
                st.warning("Niciun diagnostic sigur găsit.")

            if possible_diagnoses:
                st.info(f"Alte diagnostice posibile: {', '.join(possible_diagnoses)}")
            else:
                st.info("Nu există alte diagnostice posibile.")

with tab2:
    with tab2:
        st.subheader("Vizualizare istoric medical al unui pacient")
        patient_name_for_history = st.text_input("Introduceți numele pacientului pentru istoricul medical:")
        if st.button("Afișați Istoricul Medical"):
            patient = next((p for p in patients.values() if p['name'] == patient_name_for_history), None)
            if patient:
                doctor = doctors.get(patient['assignedDoctor'], None)
                doctor_name = doctor['name'] if doctor else "Doctor necunoscut"
                st.write(f"Istoricul medical al pacientului {patient['name']}:")
                st.write(f"Doctorul asociat: {doctor_name}")
                for condition in patient['conditions']:
                    st.write(
                        f"- Boala: {condition['name']}, Tratament: {condition['medication']} ({condition['duration']})")
            else:
                st.write("Pacientul nu a fost găsit.")

with tab3:
    with tab3:
        st.subheader("Vizualizare informații personale ale unui pacient")
        patient_name_for_info = st.text_input("Introduceți numele pacientului pentru informații personale:")
        if st.button("Afișați Informațiile Personale"):
            patient = next((p for p in patients.values() if p['name'] == patient_name_for_info), None)
            if patient:
                st.write(f"Informații personale pentru {patient['name']}:")
                st.write(f"Contact: {patient['contact']}")
                st.write(f"Vârstă: {patient['age']}")
                st.write(f"Sex: {patient['sex']}")
            else:
                st.write("Pacientul nu a fost găsit.")

with tab4:
    with tab4:
        st.subheader("Vizualizare informații despre un doctor")
        doctor_name_input = st.text_input("Introduceți numele doctorului pentru informații:")
        if st.button("Afișați Informațiile Doctorului"):
            doctor = next((d for d in doctors.values() if d['name'] == doctor_name_input), None)
            if doctor:
                st.write(f"Nume: {doctor['name']}")
                st.write(f"Contact: {doctor['contact']}")
                st.write(f"Specializare: {doctor['specialty']}")
                st.write(f"Rating: {doctor['rating']}")
                st.write("Abilități:")
                for skill in doctor['skills']:
                    st.write(f"- {skill}")
            else:
                st.write("Doctorul nu a fost găsit.")

with tab5:
    with tab5:
        st.subheader("Afectiuni tratate de un medicament")
        medication_input = st.text_input("Introduceți numele medicamentului:")
        if st.button("Afișați Bolile Tratate"):
            treated_diseases = get_diseases_by_medication(medication_input)
            if treated_diseases:
                st.write(", ".join(treated_diseases))
            else:
                st.write("Nu există boli tratate de acest medicament in baza.")
