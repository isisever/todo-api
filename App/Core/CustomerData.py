import json

import mysql.connector

def mysql_connection():
    return mysql.connector.connect(
        host="passgage-integrator-database",
        user="passgage",
        password="2110082061",
        database="passgage"
    )


def get_customer_data():
    conn = mysql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers where is_active = 1")
    column_names = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    result = [dict(zip(column_names, row)) for row in rows]
    cursor.close()
    conn.close()
    return result

def insert_or_update_customer_data(data):
    conn = mysql_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM personal_list WHERE registration_number = %s AND company_id = %s",
                   (data['registration_number'], data['company_id']))
    record = cursor.fetchone()

    if record:
        if record['data'] == json.dumps(data['data']):
            return 'passed'
        else:
            cursor.execute("""
                UPDATE personal_list
                SET data = %s, updated_date = NOW()
                WHERE registration_number = %s AND company_id = %s
            """, (json.dumps(data['data']), data['registration_number'], data['company_id']))
            conn.commit()
            return 'updated'
    else:
        cursor.execute("""
            INSERT INTO personal_list (company_id, registration_number, data, created_date, updated_date)
            VALUES (%s, %s, %s, NOW(), NOW())
        """, (data['company_id'], data['registration_number'], json.dumps(data['data'])))
        conn.commit()
        return 'inserted'

    cursor.close()
    conn.close()

def insert_or_update_branch(data, company_id):
    conn = mysql_connection()
    cursor = conn.cursor()

    cursor.execute( "SELECT * FROM branch_list WHERE company_id = %s AND branch_id = %s", (company_id, data['branch_id']))
    record = cursor.fetchone()

    if record:
        if record['branch_id'] == data['branch_id'] & record['branch_name'] == data['branch_name']:
            return 'passed'
        else:
            cursor.execute("""
                UPDATE branch_list
                SET branch_name = %s
                WHERE company_id = %s AND branch_id = %s
            """, ( data['branch_name']), company_id, data['branch_id'])
            conn.commit()
            return 'updated'
    else:
        cursor.execute("""
            INSERT INTO branch_list (branch_id, branch_name, company_id)
            VALUES (%s, %s, %s)
        """, ( data['branch_id'], data['branch_name'], company_id))
        conn.commit()
        return 'inserted'
def insert_or_update_department(data, company_id):
    conn = mysql_connection()
    cursor = conn.cursor()

    cursor.execute( "SELECT * FROM department_list WHERE company_id = %s AND department_id = %s", (company_id, data['department_id']))
    record = cursor.fetchone()

    if record:
        if record['department_id'] == data['department_id'] & record['department_name'] == data['department_name']:
            return 'passed'
        else:
            cursor.execute("""
                UPDATE department_list
                SET department_name = %s
                WHERE company_id = %s AND department_id = %s
            """, ( data['department_name']), company_id, data['department_id'])
            conn.commit()
            return 'updated'
    else:
        cursor.execute("""
            INSERT INTO department_list (department_id, department_name, company_id)
            VALUES (%s, %s, %s)
        """, ( data['department_id'], data['department_name'], company_id))
        conn.commit()
        return 'inserted'

def insert_or_update_title(data, company_id):
    conn = mysql_connection()
    cursor = conn.cursor()

    cursor.execute( "SELECT * FROM title_list WHERE company_id = %s AND title_id = %s", (company_id, data['title_id']))
    record = cursor.fetchone()

    if record:
        if record['title_id'] == data['title_id'] & record['title_name'] == data['title_name']:
            return 'passed'
        else:
            cursor.execute("""
                UPDATE title_list
                SET title_name = %s
                WHERE company_id = %s AND title_id = %s
            """, ( data['title_name']), company_id, data['title_id'])
            conn.commit()
            return 'updated'
    else:
        cursor.execute("""
            INSERT INTO title_list (title_id, title_name, company_id)
            VALUES (%s, %s, %s)
        """, ( data['title_id'], data['title_name'], company_id))
        conn.commit()
        return 'inserted'

def get_customer_personel_data(customer_id):
    conn = mysql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personal_list WHERE company_id = %s", (customer_id,))
    column_names = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    result = [dict(zip(column_names, row)) for row in rows]
    cursor.close()
    conn.close()
    return result


def get_branch_data(customer_id):
    conn = mysql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM branch_list WHERE company_id = %s", (customer_id,))  # customer_id'yi bir tuple içinde gönder
    column_names = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    result = [dict(zip(column_names, row)) for row in rows]
    print(result)  # Sonuçları yazdır
    cursor.close()
    conn.close()
    return result

def get_title_data(customer_id):
    conn = mysql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM title_list WHERE company_id = %s", (customer_id,))  # customer_id'yi bir tuple içinde gönder
    column_names = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    result = [dict(zip(column_names, row)) for row in rows]
    print(result)  # Sonuçları yazdır
    cursor.close()
    conn.close()
    return result

def get_department_data(customer_id):
    conn = mysql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM department_list WHERE company_id = %s", (customer_id,))  # customer_id'yi bir tuple içinde gönder
    column_names = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    result = [dict(zip(column_names, row)) for row in rows]
    print(result)  # Sonuçları yazdır
    cursor.close()
    conn.close()
    return result


def set_branch_passgage_id(branch_id, customer_id, passgage_id):
    conn = mysql_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE branch_list
        SET branch_passgage_id = %s
        WHERE company_id = %s AND branch_id = %s
    """, (passgage_id, customer_id, branch_id))
    conn.commit()
    cursor.close()
    conn.close()

def set_department_passgage_id(department_id, customer_id, passgage_id):
    conn = mysql_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE department_list
        SET department_passgage_id = %s
        WHERE company_id = %s AND department_id = %s
    """, (passgage_id, customer_id, department_id))
    conn.commit()
    cursor.close()
    conn.close()

def set_title_passgage_id(title_id, customer_id, passgage_id):
    conn = mysql_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE title_list
        SET title_passgage_id = %s
        WHERE company_id = %s AND title_id = %s
    """, (passgage_id, customer_id, title_id))
    conn.commit()
    cursor.close()
    conn.close()

def update_passgage_data(data):
    conn = mysql_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM personal_list
        WHERE registration_number = %s AND company_id = %s
    """, (data['registration_number'], data['company_id']))
    row = cursor.fetchone()
    if row is None:
        print("Error: No matching row found")
        return
    id_value = row[0]

    cursor.execute("""
        UPDATE personal_list
        SET passgage_data = %s, updated_date = NOW(), passgage_id = %s
        WHERE registration_number = %s AND company_id = %s
    """, (json.dumps(data['data']), data['id'], data['registration_number'], data['company_id']))

    conn.commit()

    set_is_sended(id_value, 1)

    cursor.close()
    conn.close()


def update_passgage_branch(data, customer_id):
    conn = mysql_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE branch_list
        SET branch_passgage_id = %s
        WHERE branch_name = %s AND company_id = %s
    """, (data['id'],data['title'].upper(),customer_id))

    conn.commit()
    cursor.close()
    conn.close()

def update_passgage_job_positions(data, customer_id):
    conn = mysql_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE title_list
        SET title_passgage_id = %s
        WHERE title_name = %s AND company_id = %s
    """, (data['id'],data['name'],customer_id))

    conn.commit()
    cursor.close()
    conn.close()

def update_passgage_department(data, customer_id):
    conn = mysql_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE department_list
        SET department_passgage_id = %s
        WHERE department_name = %s AND company_id = %s
    """, (data['id'],data['name'],customer_id))

    conn.commit()
    cursor.close()
    conn.close()

def set_is_updated(id, status):
    conn = mysql_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE personal_list
        SET is_updated = %s, updated_date = NOW()
        WHERE id = %s
    """, (status, id))
    conn.commit()
    cursor.close()
    conn.close()

def set_is_sended(id, status):
    conn = mysql_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE personal_list
        SET is_sended = %s, updated_date = NOW()
        WHERE id = %s
    """, (status, id))
    conn.commit()
    cursor.close()
    conn.close()