import streamlit as st
from  MedicalKnowledgeBaseParser import MedicalKnowledgeBaseParser

# Inițializăm parserul (presupunând că acesta este salvat într-un fișier medical_knowledge_base_parser.py)
parser = MedicalKnowledgeBaseParser('medical_knowledge_base.xml')
diseases = parser.get_diseases()
doctors = parser.get_doctors()
patients = parser.get_patients()
rules = parser.get_rules()

# Funcții ajutătoare pentru noile funcționalități
def get_diseases_by_medication(medication):
    diseases_treated = []
    for rule in rules:
        if medication in rule['if']:
            disease_id = rule['then']
            diseases_treated.append(diseases[disease_id]['name'])
    return diseases_treated

def get_doctors_by_specialty(specialty):
    return [d['name'] for d in doctors.values() if d['specialty'] == specialty]

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
# Interfața Streamlit pentru noile funcționalități

#1.Alegerea simptomelor și afișarea diagnosticului
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

#2.Istoric medical/pacient
st.header("Vizualizare Istoric Medical")
patient_name_for_history = st.text_input("Introduceți numele pacientului pentru istoricul medical:")
if st.button("Afișați Istoricul Medical"):
    patient = next((p for p in patients.values() if p['name'] == patient_name_for_history), None)
    if patient:
        doctor = doctors.get(patient['assignedDoctor'], None)
        doctor_name = doctor['name'] if doctor else "Doctor necunoscut"
        st.write(f"Istoricul medical al pacientului {patient['name']}:")
        st.write(f"Doctorul asociat: {doctor_name}")
        for condition in patient['conditions']:
            st.write(f"- Boala: {condition['name']}")
            st.write(f"- Tratament: {condition['medication']} ({condition['duration']})")
    else:
        st.write("Pacientul nu a fost găsit.")

#2.1Informatii personale pacient
st.header("Vizualizare Informații Personale ale Pacientului")
patient_name_for_info = st.text_input("Introduceți numele pacientului pentru informații personale:")
if st.button("Afișați Informațiile Personale"):
    patient = next((p for p in patients.values() if p['name'] == patient_name_for_info), None)
    if patient:
        st.write(f"Informații personale pentru {patient['name']}:")
        st.write(f"Contact: {patient['contact']}")
        st.write(f"Vârstă: {patient['age']}")
        st.write(f" Sex: {patient['sex']}")
    else:
        st.write("Pacientul nu a fost găsit.")

# 3. Afișarea informațiilor despre doctor
st.header("Informații despre Doctor")
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

# 4. Afișarea doctorilor pe specializare
st.header("Doctori pe Specializare")
selected_specialty = st.selectbox("Selectați specializarea:", list(set(d['specialty'] for d in doctors.values())))
if st.button("Afișați Doctorii"):
    doctors_list = get_doctors_by_specialty(selected_specialty)
    if doctors_list:
        st.write(", ".join(doctors_list))
    else:
        st.write("Nu există doctori pentru această specializare.")

# 5. Afișarea bolilor tratate de un medicament
st.header("Boli tratate de un Medicament")
medication_input = st.text_input("Introduceți numele medicamentului:")
if st.button("Afișați Bolile Tratate"):
    treated_diseases = get_diseases_by_medication(medication_input)
    if treated_diseases:
        st.write(", ".join(treated_diseases))
    else:
        st.write("Nu există boli tratate de acest medicament in baza de date.")
