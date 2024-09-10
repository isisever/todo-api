from marshmallow import Schema, fields
import os

endpoint = os.getenv('USER_ENDPOINT')
class User(Schema):

    email = fields.Email(required=True) # email veya gsm olarak nitelendirilebilir
    password = fields.String(required=True) # şifre
    password_confirmation = fields.String(required=True) # şifre tekrarı
    first_name = fields.String(required=False) # ad
    last_name = fields.String(required=False)   # soyad
    job_position_id = fields.String(required=False) # iş pozisyonu id'si
    activation_date = fields.String(required=False) # işe giriş tarihi
    citizenship_number = fields.String(required=False) # tc kimlik numarası
    department_id = fields.String(required=False) # departman id'si
    username = fields.String(required=False) # kullanıcı adı
    about = fields.String(required=False) # hakkında
    is_active = fields.Boolean(required=False) # aktif mi
    client_id = fields.String(required=False) # sicil numarası
    employee_id = fields.String(required=False) # çalışanın firma id'si
    gender = fields.String(required=False) # cinsiyet
    birth_date = fields.String(required=False) # doğum tarihi
    branch_id = fields.String(required=False) # şube id'si
    sub_company_id = fields.String(required=False) # alt firma id'si
    nationality = fields.String(required=False) # uyruk
    martial_status = fields.String(required=False) # medeni durum
    number_of_children = fields.Integer(required=False) # çocuk sayısı
    educational_status = fields.String(required=False) # eğitim durumu (primary, secondary, tertiary, postgraduate)
    graduation_level = fields.String(required=False) # eğitim seviyesi
    graduation_school = fields.String(required=False) # en son mezun olduğu okul
    bank_name = fields.String(required=False) # banka adı
    account_type = fields.String(required=False) # hesap türü
    iban = fields.String(required=False) # iban
    emergency_contact_person = fields.String(required=False) # acil durumda ulaşılacak kişi
    emergency_person_proximity_degree = fields.String(required=False) # acil durumda ulaşılacak kişinin yakınlık derecesi
    emergency_contact_person_1 = fields.String(required=False) # acil durumda ulaşılacak kişi 1
    emergency_person_proximity_degree_1 = fields.String(required=False) # acil durumda ulaşılacak kişinin yakınlık derecesi 1
    emergency_contact_phone = fields.String(required=False) # acil durumda ulaşılacak kişinin telefon numarası
    other_gsm = fields.String(required=False) # acil durumda ulaşılacak diğer kişinin telefon numarası
    organization_unit_id = fields.String(required=False) # organizasyon birimi id'si
    title_id = fields.String(required=False) # unvan id'si
    expired_date = fields.String(required=False) # işten çıkış tarihi
    reason_for_leave_id = fields.String(required=False) # işten çıkış nedeni id'si
    shift_id = fields.String(required=False) # Webshift or Pacs
    faculty_name = fields.String(required=False) # fakülte adı
    university_department = fields.String(required=False) # üniversite bölümü
    employee_type = fields.String(required=False) # öğrenci için kullanıcı tipi
    supervisor_registration_number = fields.String(required=False) # yönetici sicil numarası
    branch_name = fields.String(required=False) # şube adı
    branch_code = fields.String(required=False) # şube kodu
    group_name = fields.String(required=False)  # grup adı
    group_code = fields.String(required=False)  # grup kodu
    department_name = fields.String(required=False) # departman adı
    department_code = fields.String(required=False) # departman kodu
    job_position_name = fields.String(required=False)   # iş pozisyonu adı
    job_position_code = fields.String(required=False)   # iş pozisyonu kodu
    title_name = fields.String(required=False)  # unvan adı
    title_code = fields.String(required=False)  # unvan kodu
    sub_company_name = fields.String(required=False)    # alt firma adı
    sub_company_code = fields.String(required=False)    # alt firma kodu
    device_name = fields.String(required=False)
    device_code = fields.String(required=False)
    access_zone_name = fields.String(required=False)
    access_zone_code = fields.String(required=False)

