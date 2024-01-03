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
        for doctor in self.root.findall('doctors/doctor'):
            doc_id = doctor.get('id')
            name = doctor.find('name').text if doctor.find('name') is not None else "Nume necunoscut"
            contact = doctor.find('contact').text if doctor.find('contact') is not None else "Contact necunoscut"
            skills = [skill.text for skill in doctor.findall('skills/skill')]
            rating = doctor.find('rating').text if doctor.find('rating') is not None else "Rating necunoscut"
            specialty = doctor.find('specialty').text if doctor.find(
                'specialty') is not None else "Specialitate necunoscută"

            doctors[doc_id] = {
                'name': name,
                'contact': contact,
                'skills': skills,
                'rating': rating,
                'specialty': specialty
            }
        return doctors

    def get_patients(self):
        patients = {}
        for patient in self.root.findall('patients/patient'):
            pat_id = patient.get('id')
            name = patient.find('name').text if patient.find('name') is not None else "Nume necunoscut"
            contact = patient.find('contact').text if patient.find('contact') is not None else "Contact necunoscut"
            age = patient.find('age').text if patient.find('age') is not None else "Vârstă necunoscută"
            sex = patient.find('sex').text if patient.find('sex') is not None else "Sex necunoscut"
            assigned_doctor = patient.find('medical_history/assignedDoctor').text if patient.find(
                'medical_history/assignedDoctor') is not None else "Doctor necunoscut"

            conditions = []
            for condition in patient.findall('medical_history/conditions/condition'):
                condition_name = condition.find('name').text if condition.find(
                    'name') is not None else "Condiție necunoscută"
                medication = condition.find('treatment/medication').text if condition.find(
                    'treatment/medication') is not None else "Medicație necunoscută"
                duration = condition.find('treatment/duration').text if condition.find(
                    'treatment/duration') is not None else "Durată necunoscută"
                conditions.append({'name': condition_name, 'medication': medication, 'duration': duration})

            patients[pat_id] = {
                'name': name,
                'contact': contact,
                'age': age,
                'sex': sex,
                'assignedDoctor': assigned_doctor,
                'conditions': conditions
            }
        return patients

    def get_rules(self):
        rules = []
        for rule in self.root.findall('rules/rule'):
            if_conditions = []
            for symptom in rule.findall('if/symptom'):
                if_conditions.append(symptom.text)
            for medication in rule.findall('if/medication'):
                if_conditions.append(medication.text)

            then_conditions = [then.text.split('=')[1].replace('"', '') for then in rule.findall('then')]

            for then_condition in then_conditions:
                rules.append({'if': if_conditions, 'then': then_condition})

        return rules

    def get_investigations(self):
        investigations = {}
        for inv in self.root.findall('investigations/investigation'):
            inv_id = inv.get('id')
            name = inv.get('name')
            description = inv.find('description').text
            required_equipment = inv.find('requiredEquipment').text
            typical_duration = inv.find('typicalDuration').text

            investigations[inv_id] = {
                'name': name,
                'description': description,
                'requiredEquipment': required_equipment,
                'typicalDuration': typical_duration
            }
        return investigations

    def get_investigation_rules(self):
        invest_rules = []
        for rule in self.root.findall('invest_rules/rule'):
            if_conditions = []
            then_action = None

            # Procesarea condițiilor "if" pentru atributele pacienților
            for condition in rule.findall('if/patientAttribute'):
                attribute = condition.text
                value = rule.find(f"if/value[@for='{attribute}']").text if rule.find(
                    f"if/value[@for='{attribute}']") is not None else None
                comparison = rule.find(f"if/comparison[@for='{attribute}']").text if rule.find(
                    f"if/comparison[@for='{attribute}']") is not None else None
                if value and comparison:
                    if_conditions.append((attribute, comparison, value))

            # Procesarea acțiunii "then"
            then_element = rule.find('then')
            if then_element is not None:
                then_action = then_element.text.split('=')[1].replace('"', '').strip()

            invest_rules.append({'if': if_conditions, 'then': then_action})

        return invest_rules


