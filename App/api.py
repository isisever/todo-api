import json

import unidecode
from flask import Flask, request, jsonify, abort
from flask.views import MethodView
from flask_smorest import Api, Blueprint
import warnings
from urllib3.exceptions import NotOpenSSLWarning
import logging
from itsdangerous import URLSafeTimedSerializer as Serializer
from functools import wraps
from Core.schemas import *
from datetime import datetime
import pytz
import requests

logging.captureWarnings(True)
warnings.simplefilter('ignore', NotOpenSSLWarning)

server = Flask(__name__)

class APIConfig:
    API_TITLE = 'Passgage Integrator API'
    API_VERSION = 'v1'
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_JSON_PATH = "api-spec.json"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_RAPIDOC_PATH = "/rapidoc"
    OPENAPI_RAPIDOC_URL = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"
    OPENAPI_SECURITY_SCHEMES = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    OPENAPI_SECURITY_REQUIREMENTS = [
        {"bearerAuth": []}
    ]

server.config.from_object(APIConfig)
server.secret_key = 'E493947DA2E0495098DE60D81B560F3C'
s = Serializer(server.secret_key)

api = Api(server)
api.spec.components.security_schemes = server.config['OPENAPI_SECURITY_SCHEMES']
api.spec.security = server.config['OPENAPI_SECURITY_REQUIREMENTS']

PassgageApi = Blueprint('Passgage', 'Passgage', url_prefix='/api', description='Operations on integration')

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            abort(401, description="Authorization header is missing")

        parts = auth_header.split()

        if parts[0].lower() != 'bearer':
            abort(401, description="Authorization header must start with Bearer")
        elif len(parts) == 1:
            abort(401, description="Token not found")
        elif len(parts) > 2:
            abort(401, description="Authorization header must be Bearer token")

        token = parts[1]
        try:
            data = s.loads(token)
        except:
            abort(401, description="Token is invalid or expired")

        return f(*args, **kwargs)

    return decorated_function

def get_customer_data():
    from Core.CustomerData import get_customer_data
    dbdata = get_customer_data()
    return dbdata

@PassgageApi.route('/')
class Index(MethodView):
    def get(self):
        return jsonify({'message': 'Welcome to Passgage API'})

@PassgageApi.route('/TestFunction')
class DBCustomerData(MethodView):
    def get(self):
        return get_customer_data()

@PassgageApi.route('/login')
class Login(MethodView):
    @PassgageApi.arguments(LoginSchema, location='json')
    def post(self, args):
        username = args['username']
        password = args['password']

        if username == "savas" and password == "1234":
            token = s.dumps({'username': username})
            return jsonify({'token': token})
        else:
            abort(401, description="Unauthorized")

def APIUrlHelper(client_data ,url, method):
    if method == 'session':
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.post(url + 'IntegratorService/connect', headers = headers).json()
        return url+'(S('+response['SessionID']+'))'+'/IntegratorService/'
    else:
        return url

@PassgageApi.route('/GetBranch')
class GetBranch(MethodView):
    def get(self):
        data = GetBranch()
        return jsonify(data)

def GetBranch():
    from ERP.NebimV3.Integrator import Integrator
    from Core.CustomerData import insert_or_update_branch
    for customer in get_customer_data():
        integrator_url = APIUrlHelper(customer, customer['ip_address'], customer['method'])
        integrator = Integrator(integrator_url)
        data = {
            "ProcName": "usp_PassgageBranch"
        }
        branchIntegratorData = []
        if customer['method'] == 'session':
            branchData = integrator.post('/RunProc/', data).json()
            branchIntegratorData.append(branchData)
        else:
            branchData = integrator.post('/RunProc/' + customer['integrator_token'], data).json()
            branchIntegratorData.append(branchData)

        for branch in branchIntegratorData[0]:
            data = {
                "branch_id": branch['BranchCode'],
                "branch_name": branch['BranchName']
            }

            try:
               insert_data = insert_or_update_branch(data,customer['id'])
               print(insert_data)
            except Exception as e:
                print(f"An error occurred: {e}")

@PassgageApi.route('/GetDepartment')
class GetDepartment(MethodView):
    def get(self):
        data = GetDepartment()
        return jsonify(data)

def GetDepartment():
    from ERP.NebimV3.Integrator import Integrator
    from Core.CustomerData import insert_or_update_department
    for customer in get_customer_data():
        integrator_url = APIUrlHelper(customer, customer['ip_address'], customer['method'])
        integrator = Integrator(integrator_url)
        data = {
            "ProcName": "usp_PassgageDepartment"
        }
        departmentIntegratorData = []
        if customer['method'] == 'session':
            departmentData = integrator.post('/RunProc/', data).json()
            departmentIntegratorData.append(departmentData)
        else:
            departmentData = integrator.post('/RunProc/' + customer['integrator_token'], data).json()
            departmentIntegratorData.append(departmentData)

        for department in departmentIntegratorData[0]:
            data = {
                "department_id": department['JobDepartmentCode'],
                "department_name": department['JobDepartmentDescription']
            }

            try:
               insert_data = insert_or_update_department(data,customer['id'])
               print(insert_data)
            except Exception as e:
                print(f"An error occurred: {e}")

@PassgageApi.route('/GetTitle')
class GetTitle(MethodView):
    def get(self):
        data = GetTitle()
        return jsonify(data)

def GetTitle():
    from ERP.NebimV3.Integrator import Integrator
    from Core.CustomerData import insert_or_update_title
    for customer in get_customer_data():
        integrator_url = APIUrlHelper(customer, customer['ip_address'], customer['method'])
        integrator = Integrator(integrator_url)
        data = {
            "ProcName": "usp_PassgageJobTitle"
        }
        departmentIntegratorData = []
        if customer['method'] == 'session':
            departmentData = integrator.post('/RunProc/', data).json()
            departmentIntegratorData.append(departmentData)
        else:
            departmentData = integrator.post('/RunProc/' + customer['integrator_token'], data).json()
            departmentIntegratorData.append(departmentData)

        for department in departmentIntegratorData[0]:
            data = {
                "title_id": department['JobTitleCode'],
                "title_name": department['JobTitleDescription']
            }

            try:
               insert_data = insert_or_update_title(data,customer['id'])
               print(insert_data)
            except Exception as e:
                print(f"An error occurred: {e}")

@PassgageApi.route('/GetPersonalData')
class TestCustomer(MethodView):
    def get(self):
        data = GetPersonalData(isFull=True, now=datetime.now())
        return jsonify(data)

def GetPersonalData(isFull=False, now=None):
    from ERP.NebimV3.Integrator import Integrator
    from Core.CustomerData import insert_or_update_customer_data
    from datetime import datetime, timedelta
    import os
    integrators = []
    istanbul = pytz.timezone('Europe/Istanbul')
    time_str = now.strftime('%Y-%m-%d %H:%M:%S')
    integratorData = []
    for customer in get_customer_data():
        integrator_url = APIUrlHelper(customer, customer['ip_address'], customer['method'])
        print(APIUrlHelper);
        integrator = Integrator(integrator_url)
        integrators.append(integrator_url)
        now = datetime.now(pytz.timezone('Europe/Istanbul'))
        one_hour_ago = now - timedelta(hours=1)
        formatted_time = one_hour_ago.strftime('%Y-%m-%d %H:00:00')

        if(isFull == False):
            data = {
                "ProcName": "usp_PassgageIntegrationPersonalData",
                    "Parameters": [
                        {
                            "Name": "LastDate",
                            "Value": formatted_time
                        }
                    ]
            }
        else:
            data = {
                "ProcName": "usp_PassgageIntegrationPersonalData"
            }
        customer_name = customer['customer_name'].replace(' ', '_')
        if customer['method'] == 'session':
            customerData = integrator.post('/RunProc/', data).json()
            integratorData.append(customerData)
            directory = 'CustomerAPIData/GETERP/' + customer_name
            os.makedirs(directory, exist_ok=True)
            with open(directory+'/'+customer_name+'-'+time_str+'.txt', 'a') as f:
                f.write(json.dumps(customerData) + "\n")
        else:
            customerData = integrator.post('/RunProc/' + customer['integrator_token'], data).json()
            integratorData.append(customerData)
            directory = 'CustomerAPIData/GETERP/' + customer_name
            os.makedirs(directory, exist_ok=True)
            with open('CustomerAPIData/GETERP/'+customer_name+'/'+customer_name+'-'+time_str+'.txt', 'a') as f:
                f.write(json.dumps(customerData) + "\n")
        for personal in customerData:
            data = {
                "company_id": customer['id'],
                "registration_number": str(personal['client_id']),
                "data": personal
            }
            try:
                insert_or_update_customer_data(data)
            except Exception as e:
                print(f"An error occurred: {e}")

    return integratorData

def convert_date(date_str):
    if date_str is None:
        return None
    timestamp = int(date_str.strip("/Date()")) / 1000
    dt_object = datetime.fromtimestamp(timestamp)
    istanbul_tz = pytz.timezone('Europe/Istanbul')
    dt_object = dt_object.astimezone(istanbul_tz)
    if dt_object.strftime('%Y-%m-%d %H:%M:%S') == "1899-12-31 23:56:00":
        return "1900-01-01"
    else:
        return dt_object.strftime('%Y-%m-%d %H:%M:%S')

def send_user_data(api_url, token, data):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    for item in data:
        user_data = {
            "user": {
                "email": item['email'] if item['email'] else "",
                "gsm": item['gsm'] if item['gsm'] else "",
                "password": "12345678",
                "password_confirmation": "12345678",
                "first_name": item['first_name'] if item['first_name'] else "",
                "last_name": item['last_name'] if item['last_name'] else "",
                "activation_date": None if convert_date(item['activation_date']) == "1900-01-01" else convert_date(item['activation_date']),
                "citizenship_number": item['citizenship_number'] if item['citizenship_number'] else "",
                "username": item['username'] if item['username'] else unidecode((item['first_name'] + item['last_name']).lower()).replace(" ", ""),
                "about": item['about'] if item['about'] else "",
                "is_active": True if item['is_active'] == 1 else False,
                "client_id": item['client_id'] if item['client_id'] else None,
                "gender": "man" if item['gender'] == 'Erkek' else "woman",
                "birth_date": None if convert_date(item['birth_date']) == "1900-01-01" else convert_date(item['birth_date']),
                "user_type": "user",
                "nationality": item['nationality'] if item['nationality'] else "",
                "marital_status": item['martial_status'] if item['martial_status'] else "",
                "number_of_children": item['number_of_children'] if item['number_of_children'] else "",
                "educational_status": "primary" if item['educational_status'] == "Mezun" else "secondary",
                "graduation_level": item['graduation_level'] if item['graduation_level'] else "",
                "bank_name": item['bank_name'] if item['bank_name'] else "",
                "account_type": item['account_type'] if item['account_type'] else "",
                "iban": item['iban'] if item['iban'] else "",
                "emergency_contact_person": item['emergency_contact_person'] if item['emergency_contact_person'] else "",
                "emergency_person_proximity_degree": item['emergency_person_proximity_degree'] if item['emergency_person_proximity_degree'] else "",
                "emergency_contact_person_1": item['emergency_contact_person_1'] if item['emergency_contact_person_1'] else "",
                "emergency_person_proximity_degree_1": item['emergency_person_proximity_degree_1'] if item['emergency_person_proximity_degree_1'] else "",
                "emergency_contact_phone": item['emergency_contact_phone'] if item['emergency_contact_phone'] else "",
                "other_gsm": item['other_gsm'] if item['other_gsm'] else "",
                "expired_date": None if convert_date(item['expired_date']) == "1900-01-01" else convert_date(item['expired_date']),
                "faculty_name": item['faculty_name'] if item['faculty_name'] else "",
                "university_department": item['university_department'] if item['university_department'] else "",
                "employee_type": item['employee_type'] if item['employee_type'] else "",
                "supervisor_registration_number": item['supervisor_registration_number1'] if 'supervisor_registration_number1' in item else item['supervisor_registration_number'],
                "branch_name": item['branch_name'] if item['branch_name'] else "",
                "branch_code": item['branch_code'] if item['branch_code'] else "",
                "department_name": item['department_name'] if item['department_name'] else "",
                "department_code": item['department_code'] if item['department_code'] else "",
                "job_position_name": item['job_position_name'] if item['job_position_name'] else "",
                "job_position_code": item['job_position_code'] if item['job_position_code'] else "",
                "title_name": item['title_name'] if item['title_name'] else "",
                "title_code": item['title_code'] if item['title_code'] else "",
                "sub_company_name": item['sub_company_name'] if item['sub_company_name'] else "",
                "sub_company_code": item['sub_company_code'] if item['sub_company_code'] else "",
                "employee_id": item['employee_id'] if item['employee_id'] else None,
            }
        }
        if not item['email'] and not item['gsm']:
            # Her iki alan da boş, veriyi 'passeddata.txt' dosyasına yaz
            with open('passeddata.txt', 'a') as f:
                f.write(json.dumps(user_data) + "\n")
        else:
            response = requests.post(api_url, headers=headers, data=json.dumps(user_data))
            with open('gallerycrystal.txt', 'a') as f:
                f.write(response.text + "\n" + json.dumps(user_data)  + "\n" + "-------------------" + "\n")

            if response.status_code != 200:
                print(f"Error: {response.status_code}, {response.text}")
                print(f"Response: {response.json()}")
def get_passgage_users():
    customers = get_customer_data()
    from Core.CustomerData import update_passgage_data
    for customer in customers:
        customer_passgage_token = customer['passgage_token']
        base_url = 'https://andromeda.passgage.com/api/public/v1/users'
        headers = {
            'Authorization': f'Bearer {customer_passgage_token}',
            'Content-Type': 'application/json'
        }
        page = 1
        newData = []

        while True:
            response = requests.get(f'{base_url}?page={page}', headers=headers)
            passgage_datas = response.json()

            for passgage_data in passgage_datas['data']:
                data = {
                    "data" : passgage_data,
                    "id" : passgage_data['id'],
                    "registration_number" : passgage_data['client_id'],
                    "company_id" : customer['id']
                }

                try:
                    update_passgage_data(data)
                except Exception as e:
                    print(f"An error occurred: {e}")



                newData.append({
                    'id': passgage_data['id'],
                    'first_name': passgage_data['first_name'],
                    'last_name': passgage_data['last_name'],
                    'client_id': passgage_data['client_id'],
                })

            if passgage_datas['meta']['current_page'] >= passgage_datas['meta']['total_pages']:
                break
            page += 1

        remove_ids = ["1df9d14a-40aa-41d5-9319-3b5bab45b613", "1ceee44d-cdeb-47cd-a6db-0a14422b65cd",
                          "0cd79771-7bb0-4b19-b9cf-dd750a8efc1e"]

    filtered_data = [item for item in newData if item['id'] not in remove_ids]
    return filtered_data

@PassgageApi.route('/getPassgageUsers')
class GetAllData(MethodView):
    def get(self):
        data = get_passgage_users()
        return data

def updateOrCreatePassgage():
    from Core.CustomerData import get_customer_personel_data, set_is_updated, set_is_sended
    customers = get_customer_data()
    import pytz
    import os
    from datetime import datetime
    istanbul = pytz.timezone('Europe/Istanbul')
    process_date = datetime.now(istanbul).strftime('%Y-%m-%d %H:%M:%S')
    for customer in customers:
        customer_data = get_customer_personel_data(customer['id'])
        for personal in customer_data:
            item = json.loads(personal['data'])

            user_data = {
                "user": {
                    "email": item['email'] if item['email'] else "",
                    "gsm": item['gsm'] if item['gsm'] else "",
                    "password": "Fdsf23!fed",
                    "password_confirmation": "Fdsf23!fed",
                    "first_name": item['first_name'] if item['first_name'] else "",
                    "last_name": item['last_name'] if item['last_name'] else "",
                    "activation_date": None if convert_date(item['activation_date']) == "1900-01-01" else convert_date(item['activation_date']),
                    "citizenship_number": item['citizenship_number'] if item['citizenship_number'] else "",
                    "username": item['username'] if item['username'] else unidecode((item['first_name'] + item['last_name']).lower()).replace(" ", ""),
                    "about": item['about'] if item['about'] else "",
                    "is_active": True if item['is_active'] == 1 else False,
                    "client_id": item['client_id'] if item['client_id'] else None,
                    "gender": "man" if item['gender'] == 'Erkek' else "woman",
                    "birth_date": None if convert_date(item['birth_date']) == "1900-01-01" else convert_date(item['birth_date']),
                    "user_type": "user",
                    "nationality": item['nationality'] if item['nationality'] else "",
                    "marital_status": item['martial_status'] if item['martial_status'] else "",
                    "number_of_children": item['number_of_children'] if item['number_of_children'] else "",
                    "educational_status": "primary" if item['educational_status'] == "Mezun" else "secondary",
                    "graduation_level": item['graduation_level'] if item['graduation_level'] else "",
                    "bank_name": item['bank_name'] if item['bank_name'] else "",
                    "account_type": item['account_type'] if item['account_type'] else "",
                    "iban": item['iban'] if item['iban'] else "",
                    "emergency_contact_person": item['emergency_contact_person'] if item['emergency_contact_person'] else "",
                    "emergency_person_proximity_degree": item['emergency_person_proximity_degree'] if item['emergency_person_proximity_degree'] else "",
                    "emergency_contact_person_1": item['emergency_contact_person_1'] if item['emergency_contact_person_1'] else "",
                    "emergency_person_proximity_degree_1": item['emergency_person_proximity_degree_1'] if item['emergency_person_proximity_degree_1'] else "",
                    "emergency_contact_phone": item['emergency_contact_phone'] if item['emergency_contact_phone'] else "",
                    "other_gsm": item['other_gsm'] if item['other_gsm'] else "",
                    "expired_date": None if convert_date(item['expired_date']) == "1900-01-01" else convert_date(item['expired_date']),
                    "faculty_name": item['faculty_name'] if item['faculty_name'] else "",
                    "university_department": item['university_department'] if item['university_department'] else "",
                    "employee_type": item['employee_type'] if item['employee_type'] else "",
                    "supervisor_registration_number": item['supervisor_registration_number1'] if 'supervisor_registration_number1' in item else item['supervisor_registration_number'],
                    "branch_name": item['branch_name'] if item['branch_name'] else "",
                    "branch_code": item['branch_code'] if item['branch_code'] else "",
                    "department_name": item['department_name'] if item['department_name'] else "",
                    "department_code": item['department_code'] if item['department_code'] else "",
                    "job_position_name": item['job_position_name'] if item['job_position_name'] else "",
                    "job_position_code": item['job_position_code'] if item['job_position_code'] else "",
                    "title_name": item['title_name'] if item['title_name'] else "",
                    "title_code": item['title_code'] if item['title_code'] else "",
                    "sub_company_name": item['sub_company_name'] if item['sub_company_name'] else "",
                    "sub_company_code": item['sub_company_code'] if item['sub_company_code'] else "",
                    "employee_id": item['employee_id'] if item['employee_id'] else None,
                }
            }

            customer_passgage_token = customer['passgage_token']
            headers = {
                'Authorization': f'Bearer {customer_passgage_token}',
                'Content-Type': 'application/json'
            }
            customer_name = customer['customer_name'].replace(' ', '_')
            if personal['is_sended'] == 1 and personal['is_updated'] == 0:
                response = requests.put(customer['passgage_api_address'] + 'api/public/v1/users/' + personal['passgage_id'], headers=headers, data=json.dumps(user_data))
                print(response)
                directory = 'CustomerAPIData/response/' + customer_name
                os.makedirs(directory, exist_ok=True)
                with open(directory + '/' + customer_name + '-' + process_date + '-' + '.txt', 'a') as f:
                    f.write(response.text + "\n" + "-------------------" + "\n")

                directory = 'CustomerAPIData/Request/' + customer_name
                os.makedirs(directory, exist_ok=True)
                with open(directory + '/' + customer_name + '-' + process_date + '-' + '.txt', 'a') as f:
                    f.write(json.dumps(user_data) + "\n" + "-------------------" + "\n")

                if response.status_code == 200:
                    set_is_updated(personal['id'], 1)

                    directory = 'CustomerAPIData/UpdatePassgage/' + customer_name
                    os.makedirs(directory, exist_ok=True)
                    with open(directory + '/' + customer_name + '-' + process_date + '-' + '.txt', 'a') as f:
                        f.write(response.text + "\n" + json.dumps(user_data) + "\n" + "-------------------" + "\n")

                else:
                    directory = 'CustomerAPIData/Errors/' + customer_name
                    os.makedirs(directory, exist_ok=True)
                    with open(directory + '/' + customer_name + '-' + process_date + '-' + '.txt', 'a') as f:
                        f.write(response.text + "\n" + json.dumps(user_data) + "\n" + "-------------------" + "\n")
            elif personal['is_sended'] == 0 and personal['is_sended'] == 0:
                if  item['email'] and item['gsm']:
                    response = requests.post(customer['passgage_api_address'] + 'api/public/v1/users/', headers=headers,data=json.dumps(user_data))
                    print(response)
                    directory = 'CustomerAPIData/response/' + customer_name
                    os.makedirs(directory, exist_ok=True)
                    with open(directory + '/' + customer_name + '-' + process_date + '-' + '.txt', 'a') as f:
                        f.write(response.text + "\n" + json.dumps(user_data) + "\n" + "-------------------" + "\n")
                    if response.status_code == 200:
                        set_is_sended(personal['id'], 1)
                        set_is_updated(personal['id'], 1)
                        directory = 'CustomerAPIData/SetPassgage/' + customer_name
                        os.makedirs(directory, exist_ok=True)
                        with open(directory + '/' + customer_name + '-' + process_date + '-' + '.txt', 'a') as f:
                            f.write(response.text + "\n" + json.dumps(user_data) + "\n" + "-------------------" + "\n")
                    else:
                        directory = 'CustomerAPIData/Errors/' + customer_name
                        os.makedirs(directory, exist_ok=True)
                        with open(directory + '/' + customer_name + '-' + process_date + '-' + '.txt', 'a') as f:
                            f.write(response.text + "\n" + json.dumps(user_data) + "\n" + "-------------------" + "\n")

@PassgageApi.route('/setPassgageUsers')
class UpdateOrCreatePassgage(MethodView):
    def get(self):
        data = updateOrCreatePassgage()
        return data




def set_branch():
    from Core.CustomerData import get_branch_data,set_branch_passgage_id
    customers = get_customer_data()
    for customer in customers:
        customer_branch_data = get_branch_data(customer['id'])
        customer_passgage_token = customer['passgage_token']
        headers = {
            'Authorization': f'Bearer {customer_passgage_token}',
            'Content-Type': 'application/json'
        }
        for branch in customer_branch_data:
            branch_data = {
                "branch": {
                    "title": branch['branch_name'],
                    "is_active": True,
                    "client_id": branch['branch_id']
                }
            }
            if branch['branch_passgage_id'] is None:

                response = requests.post(customer['passgage_api_address'] + 'api/public/v1/branches/', headers=headers, data=json.dumps(branch_data))
            else:
                response = requests.patch(customer['passgage_api_address'] + 'api/public/v1/branches/' + branch['branch_passgage_id'], headers=headers, data=json.dumps(branch_data))

            if response.status_code == 201:
               response = response.json()
               set_branch_passgage_id(branch['branch_id'], customer['id'], response['data']['id'])
            else:
                print(response.text)
@PassgageApi.route('/setPassgageBranch')
class SetBranch(MethodView):
    def get(self):
        data = set_branch()
        return data

def get_passgage_branch():
    customers = get_customer_data()
    from Core.CustomerData import update_passgage_branch
    for customer in customers:
        customer_passgage_token = customer['passgage_token']
        base_url = customer['passgage_api_address']+'api/public/v1/branches'
        headers = {
            'Authorization': f'Bearer {customer_passgage_token}',
            'Content-Type': 'application/json'
        }
        page = 1
        newData = []

        while True:
            response = requests.get(f'{base_url}?page={page}', headers=headers)
            passgage_datas = response.json()

            for passgage_data in passgage_datas['data']:
                try:
                    update_passgage_branch(passgage_data, customer['id'])
                except Exception as e:
                    print(f"An error occurred: {e}")

                newData.append({
                    'id': passgage_data['id'],
                    'branch': passgage_data['title'],
                })

            if passgage_datas['meta']['current_page'] >= passgage_datas['meta']['total_pages']:
                break
            page += 1

        return newData


@PassgageApi.route('/getPassgageBranch')
class GetBranchData(MethodView):
    def get(self):
        data = get_passgage_branch()
        return data


def get_passgage_job_positions():
    customers = get_customer_data()
    from Core.CustomerData import update_passgage_job_positions
    for customer in customers:
        customer_passgage_token = customer['passgage_token']
        base_url = customer['passgage_api_address']+'api/public/v1/job_positions'
        headers = {
            'Authorization': f'Bearer {customer_passgage_token}',
            'Content-Type': 'application/json'
        }
        page = 1
        newData = []

        while True:
            response = requests.get(f'{base_url}?page={page}', headers=headers)
            passgage_datas = response.json()

            for passgage_data in passgage_datas['data']:
                try:
                    update_passgage_job_positions(passgage_data, customer['id'])
                except Exception as e:
                    print(f"An error occurred: {e}")

                newData.append({
                    'id': passgage_data['id'],
                    'title': passgage_data['name'],
                })

            if passgage_datas['meta']['current_page'] >= passgage_datas['meta']['total_pages']:
                break
            page += 1

        return newData


@PassgageApi.route('/getPassgageJobPositions')
class GetBranchData(MethodView):
    def get(self):
        data = get_passgage_job_positions()
        return data



def set_branch():
    from Core.CustomerData import get_branch_data,set_branch_passgage_id
    customers = get_customer_data()
    for customer in customers:
        customer_branch_data = get_branch_data(customer['id'])
        customer_passgage_token = customer['passgage_token']
        headers = {
            'Authorization': f'Bearer {customer_passgage_token}',
            'Content-Type': 'application/json'
        }
        for branch in customer_branch_data:
            branch_data = {
                "branch": {
                    "title": branch['branch_name'],
                    "is_active": True,
                    "client_id": branch['branch_id']
                }
            }
            if branch['branch_passgage_id'] is None:

                response = requests.post(customer['passgage_api_address'] + 'api/public/v1/branches/', headers=headers, data=json.dumps(branch_data))
            else:
                response = requests.patch(customer['passgage_api_address'] + 'api/public/v1/branches/' + branch['branch_passgage_id'], headers=headers, data=json.dumps(branch_data))

            if response.status_code == 201:
               response = response.json()
               set_branch_passgage_id(branch['branch_id'], customer['id'], response['data']['id'])
            else:
                print(response.text)
@PassgageApi.route('/setPassgageBranch')
class SetBranch(MethodView):
    def get(self):
        data = set_branch()
        return data



def set_job_positions():
    from Core.CustomerData import get_title_data,set_title_passgage_id
    customers = get_customer_data()
    for customer in customers:
        customer_job_position_data = get_title_data(customer['id'])
        customer_passgage_token = customer['passgage_token']
        headers = {
            'Authorization': f'Bearer {customer_passgage_token}',
            'Content-Type': 'application/json'
        }
        for job_positions in customer_job_position_data:
            job_position_data = {
                "job_position": {
                    "name": job_positions['title_name'],
                    "is_active": True,
                    "client_id": job_positions['title_id']
                }
            }
            print(job_position_data)
            if job_positions['title_passgage_id'] is None:
                response = requests.post(customer['passgage_api_address'] + 'api/public/v1/job_positions/', headers=headers, data=json.dumps(job_position_data))
            else:
                response = requests.patch(customer['passgage_api_address'] + 'api/public/v1/job_positions/' + job_positions['title_passgage_id'], headers=headers, data=json.dumps(job_position_data))

            if response.status_code == 201:
               response = response.json()
               set_title_passgage_id(job_positions['title_id'], customer['id'], response['data']['id'])
            else:
                print(response.text)
@PassgageApi.route('/setPassgageJobPositions')
class SetBranch(MethodView):
    def get(self):
        data = set_job_positions()
        return data




def get_passgage_departments():
    customers = get_customer_data()
    from Core.CustomerData import update_passgage_department
    for customer in customers:
        customer_passgage_token = customer['passgage_token']
        base_url = customer['passgage_api_address']+'api/public/v1/departments'
        headers = {
            'Authorization': f'Bearer {customer_passgage_token}',
            'Content-Type': 'application/json'
        }
        page = 1
        newData = []

        while True:
            response = requests.get(f'{base_url}?page={page}', headers=headers)
            passgage_datas = response.json()

            for passgage_data in passgage_datas['data']:
                try:
                    update_passgage_department(passgage_data, customer['id'])
                except Exception as e:
                    print(f"An error occurred: {e}")

                newData.append({
                    'id': passgage_data['id'],
                    'title': passgage_data['name'],
                })

            if passgage_datas['meta']['current_page'] >= passgage_datas['meta']['total_pages']:
                break
            page += 1

        return newData


@PassgageApi.route('/getPassgageDepartments')
class GetBranchData(MethodView):
    def get(self):
        data = get_passgage_departments()
        return data


def set_departments():
    from Core.CustomerData import get_department_data,set_department_passgage_id
    customers = get_customer_data()
    for customer in customers:
        customer_job_position_data = get_department_data(customer['id'])
        customer_passgage_token = customer['passgage_token']
        headers = {
            'Authorization': f'Bearer {customer_passgage_token}',
            'Content-Type': 'application/json'
        }
        for departments in customer_job_position_data:
            job_position_data = {
                "department": {
                    "name": departments['department_name'],
                    "is_active": True,
                    "client_id": departments['department_id']
                }
            }
            print(job_position_data)
            if departments['department_passgage_id'] is None:
                response = requests.post(customer['passgage_api_address'] + 'api/public/v1/departments/', headers=headers, data=json.dumps(job_position_data))
            else:
                response = requests.patch(customer['passgage_api_address'] + 'api/public/v1/departments/' + departments['department_passgage_id'], headers=headers, data=json.dumps(job_position_data))

            if response.status_code == 201:
               response = response.json()
               set_department_passgage_id(departments['department_id'], customer['id'], response['data']['id'])
            else:
                print(response.text)
@PassgageApi.route('/setPassgageDepartments')
class SetBranch(MethodView):
    def get(self):
        data = set_departments()
        return data



api.register_blueprint(PassgageApi)

if __name__ == '__main__':
    server.run(debug=True)
