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

        if config.loglevel == logging.DEBUG:
            logging.debug("\n\n\nhive_row = {}\n\n\n".format(json.dumps(hive_row)))

        if config.loglevel == logging.DEBUG:
            logging.debug("hive_row = {}".format(json.dumps(hive_row)))

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


        formatted_hive_row = hive_row

        formatted_hive_row_cleaned = {k:v for k,v in formatted_hive_row.iteritems() if v is not None and v != "None"}

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

    wat = WebAnalyticsTransformer()
    wat.convert_hive_row_to_keen_format(hive_row)
