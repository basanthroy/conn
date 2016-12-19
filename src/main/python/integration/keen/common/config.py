__author__ = 'broy'

import logging

keen_api_event_header_template={"Authorization": "KEEN_CUSTOM_KEY", "Content-Type" : "application/json"}
keen_api_template = """https://api.keen.io/3.0/projects/{}/events"""

# personal mac
# BASE_DIR='/Users/broy/keen'
# jobserver2/connu
BASE_DIR='/opt/dwradiumone/r1-dw-mobile-lowlatency-app/test/web_analytics'
ROOT_DIR=BASE_DIR + '/log/rt'
SCRIPT_DIR=BASE_DIR + '/scripts/src/main/python/integration/keen'

report_db_connect_host = 'que1.dw.sc.gwallet.com'
report_db_connect_user = 'connu'
report_db_connect_password = 'D3BFgfhEBSIo'
report_db_connect_db = 'test_connect'

app_db_connect_host = 'que1.dw.sc.gwallet.com'
app_db_connect_user = 'connu'
app_db_connect_password = 'D3BFgfhEBSIo'
app_db_connect_db = 'test_connect'

#app_db_connect_host = 'connect.dmp.dw.sc.gwallet.com'
#app_db_connect_user = 'broy'
#app_db_connect_password = 'uaMo7eiGhee8ria'
#app_db_connect_db = 'connect_production'

hive_server_host = 'jobserver.dw.sc.gwallet.com'
hive_server_user = 'dtopsu'
hive_server_password = 'dtopsu'
hive_server_port = 10000
hive_server_auth = 'PLAIN'

loglevel = logging.DEBUG

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

keen_metadata_wa = """
    {"timestamp": "TIMESTAMP_PLACEHOLDER",
     "addons" : [
          {
            "name" : "keen:url_parser",
            "input" : {
              "url" : "url"
            },
            "output" : "parsed_page_url"
          },
          {
            "name" : "keen:ip_to_geo",
            "input" : {
              "ip" : "ip"
            },
            "output" : "parsed_ip_geo"
          },
          {
            "name" : "keen:referrer_parser",
            "input" : {
              "referrer_url" : "referrer",
              "page_url" : "url"
            },
            "output" : "parsed_referrer_url"
          },
          {
            "name" : "keen:ua_parser",
            "input" : {
              "ua_string" : "user_agent"
            },
            "output" : "parsed_user_agent"
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

max_concurrent_python_processes_on_server=8

debug_app_id_list = []
