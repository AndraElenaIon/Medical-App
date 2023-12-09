import streamlit as st
from  MedicalKnowledgeBaseParser import MedicalKnowledgeBaseParser

# Inițializăm parserul (presupunând că acesta este salvat într-un fișier medical_knowledge_base_parser.py)
parser = MedicalKnowledgeBaseParser('medical_knowledge_base.xml')
diseases = parser.get_diseases()
doctors = parser.get_doctors()
patients = parser.get_patients()
rules = parser.get_rules()

# Functie pentru determinarea diagnosticului
def get_diagnosis(selected_symptoms):
    certain_diagnosis = None
    possible_diagnoses = set()

    for disease_id, disease_info in diseases.items():
        disease_symptoms = set(disease_info['symptoms'])
        selected_symptoms_set = set(selected_symptoms)

        if disease_symptoms == selected_symptoms_set:
            certain_diagnosis = disease_info['name']
        elif selected_symptoms_set.issubset(disease_symptoms) or disease_symptoms.issubset(selected_symptoms_set):
            possible_diagnoses.add(disease_info['name'])

    # Eliminăm diagnosticul sigur din diagnosticele posibile, dacă există
    possible_diagnoses.discard(certain_diagnosis)

    return certain_diagnosis, list(possible_diagnoses)


# Interfața Streamlit
st.title("Sistem de Interogare a Bazei de Cunoștințe Medicale")

# Alegerea simptomelor și afișarea diagnosticului
st.header("Diagnosticare pe baza simptomelor")
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

# Afișarea doctorului pentru un pacient
st.header("Aflați doctorul asociat unui pacient")
patient_name = st.text_input("Introduceți numele pacientului:")
if st.button("Afișați Doctorul"):
    patient = next((p for p in patients.values() if p['name'] == patient_name), None)
    if patient:
        doctor = doctors[patient['assignedDoctor']]
        st.write(f"Doctorul asociat este: {doctor['name']} ({doctor['specialty']})")
    else:
        st.write("Pacientul nu a fost găsit.")

# Afișarea pacienților unui doctor și specializarea acestuia
st.header("Afișați pacienții unui doctor și specializarea acestuia")
doctor_name = st.selectbox("Selectați doctorul:", [d['name'] for d in doctors.values()])
if st.button("Afișați Pacienții"):
    selected_doctor = next((doc_id for doc_id, d in doctors.items() if d['name'] == doctor_name), None)
    if selected_doctor:
        associated_patients = [p['name'] for p in patients.values() if p['assignedDoctor'] == selected_doctor]
        st.write(f"Pacienți asociati cu Dr. {doctor_name}: {', '.join(associated_patients)}")
        st.write(f"Specializarea: {doctors[selected_doctor]['specialty']}")
