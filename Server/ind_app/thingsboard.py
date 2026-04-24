import base64

import psycopg2
import pytz
from _datetime import datetime
import json


# HOST = '192.168.100.50'


class TBHelper():
    def __init__(self):
        self.conn = psycopg2.connect(database="thingsboard", user="postgres", password="Cybershot#903",
                                     host="localhost",
                                     port=5432)
        self.c = self.conn.cursor()
        if not self.conn.closed:
            print("Connection established!")

        print("the connection is :--", self.conn)

    def reset_password_by_id(self, reset_id: str):
        '''
        This will update the data from user_credentials table by ID, Columns Activated token, enabled should be true
        and password will be set to Null

        :param reset_id:
        :return activated_token:
        '''

        # current_datetime = datetime.now()
        # datetime_bytes = current_datetime.strftime('%Y-%m-%d %H:%M:%S').encode('utf-8')
        # activated_token = base64.b64encode(datetime_bytes)

        uuid_without_hyphens = reset_id.replace("-", "")
        # uuid_bytes = bytes.fromhex(uuid_without_hyphens)
        # activated_token = base64.b64encode(uuid_bytes).decode("utf-8")
        base64_string = base64.b64encode(bytes.fromhex(uuid_without_hyphens)).decode('ascii')
        activated_token = ''.join(c for c in base64_string if c.isalnum())

        enabled = False
        password = None

        # Update in db

        update_query = """
            UPDATE user_credentials
            SET activate_token = %s, enabled = %s, password = %s
            WHERE user_id = %s
        """
        self.c.execute(update_query, (activated_token, enabled, password, reset_id))
        self.conn.commit()
        return activated_token

    def __del__(self):
        self.conn.close()

# if __name__ == '__main__':
#     c = TBHelper()
#     check = c.get_user_added_audit(from_=1681123873230, to_=1682942415986)
#     print("lenght of the list: " + str(len(check)))
#     # for i in range(len(check)):
#     #     input_str = check[i][5]
#     #     json_data = json.loads(input_str.replace("'", '"'))
#     #     title_param = c.get_tilte_from_cust_id(cust_id=json_data['entity']['customerId']['id'])
#     #     print("Cutomer_id: " + json_data['entity']['customerId']['id'] + "title: " + title_param[0][0])
#     print(check)

# self.c.execute(f'''SELECT email FROM tb_user
#                         WHERE customer_id ='{customer_id}';''')
# result_3 = self.c.fetchall()
# res_3 = [x[0] for x in result_3]
# print("The user_name is:--", res_3)

# self.c.execute('''SELECT email from customer;''')
# result_5 = self.c.fetchall()
# res_5 = [x[0] for x in result_5]
# print("The customer_email of customer table is:--", res_5)
#
# self.c.execute('''SELECT id from customer;''')
# result_6 = self.c.fetchall()
# res_6 = [x[0] for x in result_6]
# print("The customer_id of customer table is:--", res_6)

# self.c.execute(f'''SELECT email from customer
#                    WHERE id ='{customer_id}';''')
# users = self.c.fetchall()
# # print("ips", users)
# users_names=[x[0] for x in users]
# print("users are :--",users_names)

# def get_entity_name_of_audit_log(self,customer_id):
#
#     self.c.execute(f'''SELECT entity_name from audit_log
#                                WHERE customer_id ='{customer_id}';''')
#     users = self.c.fetchall()
#     # print("ips", users)
#     users_names = [x[0] for x in users]
#     print("users are audit log :--", users_names)

# c = TBHelper()
# print(c)

# result = c.get_attributes_from_tb_user('77ec2740-d4e4-11ec-ac68-ada1134c95b7')
# result_2 = c.get_user_from_tb_user('77ec2740-d4e4-11ec-ac68-ada1134c95b7')
# result_3 = c.get_entity_name_of_audit_log('77ec2740-d4e4-11ec-ac68-ada1134c95b7')

# def get_attributes(self, entity_id, name):
#     self.c.execute(f'''SELECT str_v from attribute_kv
#                 WHERE entity_id ='{entity_id}' AND attribute_key ='ip_address';''')
#     ips = self.c.fetchall()
#     for ip in ips:
#         self.machine_data[name]['ip'] = ip[0]
#     self.c.execute(f'''SELECT long_v from attribute_kv
#                     WHERE entity_id ='{entity_id}' AND attribute_key ='port';''')
#     ports = self.c.fetchall()
#     for port in ports:
#         self.machine_data[name]['port'] = port[0]
#
#     self.c.execute(f'''SELECT credentials_id from device_credentials
#                     WHERE device_id ='{entity_id}' AND credentials_type ='ACCESS_TOKEN';''')
#     tokens = self.c.fetchall()
#     for token in tokens:
#         self.machine_data[name]['accessToken'] = token[0]
#
#     self.c.execute(f'''SELECT bool_v from attribute_kv
#                         WHERE entity_id ='{entity_id}' AND attribute_key ='connect';''')
#     connects = self.c.fetchall()
#     for connect in connects:
#         self.machine_data[name]['connect'] = 1 if connect[0] else 0
#
#
# def getMachineData(self):
#     self.machine_data = {}
#     self.c.execute(f"SELECT id,name,label from device WHERE type = 'grinder';")
#     fetched = self.c.fetchall()
#     for id, name, label in fetched:
#         self.machine_data[name] = {'machineId': label, 'machineName': name, 'unitId': 1}
#         self.get_attributes(id, name)
