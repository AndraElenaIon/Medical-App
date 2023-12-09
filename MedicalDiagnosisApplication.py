from MedicalKnowledgeBaseParser import MedicalKnowledgeBaseParser

parser = MedicalKnowledgeBaseParser('medical_knowledge_base.xml')
diseases = parser.get_diseases()
doctors = parser.get_doctors()
patients = parser.get_patients()
rules = parser.get_rules()


def get_diseases_by_medication(medication):
    diseases_treated = []
    for rule in rules:
        if medication in rule['if']:
            disease_id = rule['then']
            diseases_treated.append(diseases[disease_id]['name'])
    return diseases_treated


def get_doctors_by_specialty(specialty):
    return [d['name'] for d in doctors.values() if d['specialty'] == specialty]


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

    possible_diagnoses.discard(certain_diagnosis)

    return certain_diagnosis, list(possible_diagnoses)
