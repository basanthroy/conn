__author__ = 'broy'

import logging

keen_api_event_header_template={"Authorization": "KEEN_CUSTOM_KEY", "Content-Type" : "application/json"}
keen_api_template = """https://api.keen.io/3.0/projects/{}/events"""

# personal mac
# ROOT_DIR='/Users/broy/keen/log/rt'
# jobserver2/connu
ROOT_DIR='/opt/dwradiumone/r1-dw-connect-app/dev/tracker_event_stj/log/rt'

report_db_connect_host = 'que2.dw.sc.gwallet.com'
report_db_connect_user = 'arteu'
report_db_connect_password = 'arteu1arteu'
report_db_connect_db = 'test_connect'

app_db_connect_host = 'ec2-54-175-102-162.compute-1.amazonaws.com'
app_db_connect_user = 'readonly'
app_db_connect_password = 'WBmPY4rzNpR5'
app_db_connect_db = 'connect_production_v3'

hive_server_host = 'jobserver.dw.sc.gwallet.com'
hive_server_user = 'bruderman'
hive_server_password = 'brad'
hive_server_port = 10000
hive_server_auth = 'PLAIN'

loglevel = logging.INFO

keen_payload_record_batch_size=2000
hive_queries_throttle_batch_size=20
hive_queries_date_range=31

keen_metadata = """
    {"timestamp": "TIMESTAMP_PLACEHOLDER",
     "addons" : [
         {"name" : "keen:ip_to_geo",
          "input" : {
              "ip" : "ip_address"
          },
          "output" : "ip_geo_info"
         }
     ]
    }
"""

klass = "class"
hive_db = "hive_db"
hive_table = "hive_table"
hive_line_parser="hive_line_parser"
keen_collection = "keen_collection"
keen_collection_name_function = "lamda"
file_list_retriever="file_list_retriever"
entity_base_dir_template="entity_base_dir_template"
entity_filepath_template="entity_filepath_template"

debug_app_id_list = []