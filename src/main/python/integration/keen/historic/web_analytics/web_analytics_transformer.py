__author__ = 'broy'

import integration.keen.common.config
import json
import logging
import re
from time import gmtime, strftime

from integration.keen.common import config
from integration.keen.historic.common.transformer import Transformer


class WebAnalyticsTransformer(Transformer):

    def convert_hive_row_to_keen_format(self, hive_row):

        if hive_row["tracking_id"] in config.debug_app_id_list:
            logging.info("DEBUG APP_ID, app_id = {}, hive_row={}"
                         .format(hive_row["tracking_id"], hive_row))

        # logging.info("TrackerEventTSTransformer, hive_row = {}".format(hive_row))
        if config.loglevel == logging.DEBUG:
            logging.debug("\n\n\nhive_row = {}\n\n\n".format(json.dumps(hive_row)))

        # if type(hive_row["message"]) == str:
        #     hive_row["message"] = json.loads(hive_row["message"])

        if config.loglevel == logging.DEBUG:
            logging.debug("hive_row = {}".format(json.dumps(hive_row)))

        # formatted_hive_row = {str(key): str(value) for key, value in hive_row["message"].iteritems()
        #                       if type(value) != dict}
        #
        # for k, v in dict(hive_row).iteritems():
        #     if type(k) != dict and k != "message":
        #         formatted_hive_row[str(k)] = str(v)
        #
        # device_info = hive_row["message"]["device_info"]
        # for k, v in dict(device_info).iteritems():
        #     if type(k) != dict and k != "id_info":
        #         formatted_hive_row[str(k)] = str(v)
        #
        # id_info = device_info["id_info"]
        #
        # for k, v in dict(id_info).iteritems():
        #     if (type(k) != dict):
        #         formatted_hive_row[str(k)] = str(v)

        #
        # event_attr_dicts = [v for k, v in dict(hive_row["message"]["event"]).iteritems() if type(v) is dict]
        # for kv_inner in list(event_attr_dicts):
        #     if config.loglevel == logging.DEBUG:
        #         logging.debug("kv_inner = {}".format(kv_inner))
        #     for inner_key, inner_value in kv_inner.iteritems():
        #         if (type(inner_value) is not dict and type(inner_value) is not list):
        #             formatted_hive_row[str(inner_key)] = str(inner_value)
        #
        # if not formatted_hive_row.has_key("ip_address") or formatted_hive_row["ip_address"] == "127.0.0.1":
        #     if formatted_hive_row.has_key("x_forwarded_for") and not formatted_hive_row["x_forwarded_for"] == "127.0.0.1":
        #         formatted_hive_row["ip_address"] = formatted_hive_row["x_forwarded_for"]
        # # formatted_hive_row["ip_address"] = ".".join(formatted_hive_row["ip_v4"].split(".")[:4])


        if hive_row.has_key("json_data"):
            json_data = hive_row["json_data"]
            json_data = json.loads(json_data)

            logging.error("JSON_DATA={}".format(json_data))

            hive_row.update(json_data)
            del hive_row["json_data"]

        if hive_row.has_key("eventInfo") and type(hive_row["eventInfo"]) == list:
            eventInfo = hive_row["eventInfo"][0]
            hive_row.update({k:v for k,v in eventInfo.iteritems() if (type(v) is not dict and type(v) is not list)})
            if eventInfo.has_key("keyValue"):
                keyValue = eventInfo["keyValue"]
                #hive_row.update({k:v for kv in  dict(kv) for kv in keyValue})
                for kv in keyValue:
                    if kv.has_key("key") and kv.has_key("stringValue"):
                        hive_row.update({kv["key"]:kv["stringValue"]})
            if eventInfo.has_key("pageInfo"):
                pageInfo = eventInfo["pageInfo"]
                hive_row.update({k:v for k,v in pageInfo.iteritems()})
            del hive_row["eventInfo"]

        if hive_row.has_key("deviceInfo") and hive_row["deviceInfo"].has_key("idInfo"):
            hive_row.update({k:v for k,v in hive_row["deviceInfo"]["idInfo"].iteritems()})
        if hive_row.has_key("deviceInfo") and hive_row["deviceInfo"].has_key("screen"):
            hive_row.update({"screen" + k:v for k,v in hive_row["deviceInfo"]["screen"].iteritems()})
        del hive_row["deviceInfo"]

        if hive_row.has_key("page"):
            hive_row.update({k:v for k,v in hive_row["page"].iteritems()})
        del hive_row["page"]

        if hive_row.has_key("eventName"):
            hive_row["event_name"] = hive_row["eventName"]
            del hive_row["eventName"]
        if hive_row.has_key("applicationName"):
            hive_row["application_name"] = hive_row["applicationName"]
            del hive_row["applicationName"]
        if hive_row.has_key("applicationVersion"):
            hive_row["application_version"] = hive_row["applicationVersion"]
            del hive_row["applicationVersion"]
        if hive_row.has_key("transactionId"):
            hive_row["transaction_id"] = hive_row["transactionId"]
            del hive_row["transactionId"]



        #     and hive_row["message"]["event"].has_key("key_value"):
        #     event_kv = hive_row["message"]["event"]["key_value"]
        #
        #     for kv in list(event_kv if event_kv is not None else []):
        #         if config.loglevel == logging.DEBUG:
        #             logging.debug("key value={}".format(kv))
        #         if kv.has_key("key") and kv.has_key("string_value"):
        #             formatted_hive_row[kv["key"]] = str(kv["string_value"])
        #         if kv.has_key("key") and kv.has_key("long_value"):
        #             formatted_hive_row[kv["key"]] = str(kv["long_value"])
        #         if kv.has_key("key") and kv.has_key("double_value"):
        #             formatted_hive_row[kv["key"]] = str(kv["double_value"])
        #         if kv.has_key("key") and kv.has_key("bool_value"):
        #             formatted_hive_row[kv["key"]] = str(kv["bool_value"])
        #
        # formatted_hive_row.update({str(k): str(v) for k, v in dict(hive_row["message"]["event"]).iteritems() if
        #                            (type(v) is not dict and type(v) is not list)})

            #for k,v in json_data.iteritems():
            #    formatted_hive_row[k] = v

        ########################
        ## temporary workaround
        #if hive_row.has_key("event_info"):
        #    ei = hive_row["event_info"]
        #    if ei.has_key("event_info"):
        #        eii = ei["event_info"]
        #        if eii[0].has_key("timestamp"):
        #            hive_row["timestamp"] = eii[0]["timestamp"]
        ## temporary workaround
        ########################

        formatted_hive_row = hive_row

        formatted_hive_row_cleaned = {k:v for k,v in formatted_hive_row.iteritems() if v is not None and v != "None"}

        # if formatted_hive_row_cleaned.has_key("session_length"):
        #     formatted_hive_row_cleaned["session_length"] = int(formatted_hive_row_cleaned["session_length"])
        # if formatted_hive_row_cleaned.has_key("subsession_length"):
        #     formatted_hive_row_cleaned["subsession_length"] = int(formatted_hive_row_cleaned["subsession_length"])
        #
        # if formatted_hive_row_cleaned.has_key("installed_app_info"):
        #     del formatted_hive_row_cleaned["installed_app_info"]
     

        if formatted_hive_row_cleaned.has_key("app"):
            formatted_hive_row_cleaned.update({"app_" + k: v for k,v in formatted_hive_row_cleaned["app"].iteritems()})

        timestamp = strftime("%Y-%m-%dT%H:%M:%S.{}Z".format(str(formatted_hive_row_cleaned["timestamp"])[-3:]),
                             gmtime(int(str(formatted_hive_row["timestamp"])[:-3])))

        keen_md = json.loads(re.sub("TIMESTAMP_PLACEHOLDER", timestamp, integration.keen.common.config.keen_metadata_wa))
        if not formatted_hive_row_cleaned.has_key("ip"):
            addons = keen_md["addons"]
            addons = [addon for addon in addons if addon["name"] != "keen:ip_to_geo"]
            keen_md["addons"] = addons

        formatted_hive_row_cleaned["keen"] = keen_md

        formatted_hive_row = formatted_hive_row_cleaned

        return super(WebAnalyticsTransformer, self).cleanup(formatted_hive_row)


if __name__ == "__main__":

    f = open("sample.json")
    l = f.readline()
    # print "l == {}".format(l)
    hive_row = json.loads(l)
    # print "l == {}".format(l)

    # hive_row = "{'tracking_id':'0305A750-0DB1-4B1A-979D-9D860353A899','application_name':'ShopSavvy','application_user_id':null,'application_version':'10.6.1','application_build':'2','conn_type':'CARRIER','timezone':'America/Los_Angeles','user_language':'en_US','sdk_version':'3.3.1','source':'ADVERTISER_SDK','page':{'page':{'referrer':'http://www.radiumone.com','title':'AdTech Ninjas','url':'www.cnn.com','scroll_position':'30x40'}},'device_info':{'device_info':{'id_info':{'post_cookie':'32charactersneeded','ob_login':'ob_login_value','opt_out':false},'ip_v4':'92.117.48.48.67.48.92.117.48.48.48.48.92.117.48.48.48.48.92.117.48.48.48.52','user_agent':'Mozilla/5.0 (Linux; Android 6.0; LG-H901 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/54.0.2840.85 Mobile Safari/537.36','screen':{'width':320,'height':568,'density':2,'viewport_size':'1440x2392'}}},'event_info':{'event_info':[{'event_name':'Application Opened','key_value':{'network':'RealZeit - Android','source':'RealiZeit > RealZeit - Android','id':'123','name':'Shoes','currency':'USD','receipt_status':'no_receipt'},'lat':null,'lon':null,'session_id':'1914d9c4-9615-4324-8212-ba9b8e6c7c3b','timestamp':1481546689543,'transaction_id':'92.117.48.48.70.51.92.117.48.48.70.70.92.117.48.48.65.68.92.117.48.48.54.51.92.117.48.48.66.70.92.117.48.48.55.65.92.117.48.48.52.56.92.117.48.48.53.51.92.117.48.48.56.66.92.117.48.48.48.69.92.117.48.48.51.68.92.117.48.48.49.68.92.117.48.48.48.70.92.117.48.48.65.48.92.117.48.48.66.54.92.117.48.48.55.65'}]}}"
    # hive_row = json.loads(hive_row)

    wat = WebAnalyticsTransformer()
    wat.convert_hive_row_to_keen_format(hive_row)
