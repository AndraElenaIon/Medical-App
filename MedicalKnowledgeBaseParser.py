import xml.etree.ElementTree as ET

class MedicalKnowledgeBaseParser:
    def __init__(self, xml_file):
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()

    def get_diseases(self):
        diseases = {}
        for disease in self.root.find('diseases'):
            disease_id = disease.get('id')
            name = disease.get('name')
            symptoms = [symptom.text for symptom in disease.find('symptoms')]
            diseases[disease_id] = {'name': name, 'symptoms': symptoms}
        return diseases

    def get_doctors(self):
        doctors = {}
        for doctor in self.root.find('doctors'):
            doc_id = doctor.get('id')
            name = doctor.get('name')
            specialty = doctor.get('specialty')
            doctors[doc_id] = {'name': name, 'specialty': specialty}
        return doctors

    def get_patients(self):
        patients = {}
        for patient in self.root.find('patients'):
            pat_id = patient.get('id')
            name = patient.get('name')
            assigned_doctor = patient.get('assignedDoctor')
            diagnoses = [diagnosis.text for diagnosis in patient.find('diagnoses')]
            patients[pat_id] = {'name': name, 'assignedDoctor': assigned_doctor, 'diagnoses': diagnoses}
        return patients

    def get_rules(self):
        rules = []
        for rule in self.root.find('rules'):
            if_conditions = [symptom.text for symptom in rule.find('if')]
            then_condition = rule.find('then').text.split('=')[1].replace('"', '')  # Modificat aici
            rules.append({'if': if_conditions, 'then': then_condition})
        return rules

# # Utilizarea Parser-ului
# xml_file = 'medical_knowledge_base.xml'  # Numele fișierului dvs. XML
# parser = MedicalKnowledgeBaseParser(xml_file)
#
# # Exemplu de extragere a datelor
# diseases = parser.get_diseases()
# doctors = parser.get_doctors()
# patients = parser.get_patients()
# rules = parser.get_rules()
#
# print(diseases)
# print(doctors)
# print(patients)
# print(rules)
