BROKEN - Enphase are now activley rolling out version 7 Envoy firmware which requires a time limited authentication token to access the data on our own local solar instalations. Enphase say that this improves our security however it now means we have to store our Enphase website username and pasword on our server in order to renew the token progmatically. I personally struggle to understand how this is an improvement to my security. Enphase's actions break this script and any other scripts designed for Envoy firmware earlier than version 7. I will look into how best to update this script at some point in the future but for now, if like mine, your Envoy is on version 7.x firmware, this script will no longer work for you. 

Python script to take solar data from a local Enphase Envoy and push it to the ChargeHQ API.  
Created because ChargeHQ is unable to support Enphase nativley due to Enphase 3rd party access policy.  

ChargeHQ specific information available from https://chargehq.net/kb/push-api

Known to work with version 5 Envoy firmware. 

Uses the Envoy production.json data.  

crontab to run every minute, 5AM to 10PM daily; ` */1 5-21 * * * <path>/chargehq.py` 

Requires a config.py file in the same directory with the following format;  
source = `'http://<ip of your local envoy>/production.json'`    
endPoint = `'https://api.chargehq.net/api/public/push-solar-data>'`  
apiKey = `'<your apiKey from https://app.chargehq.net/config/energy-monitor>'`

POST's the following json to ChargeHQ;  
{"apiKey": "not_telling", "siteMeters": {"production_kw": 0.00, "net_import_kw": 0.00, "consumption_kw": 0.00}}

Negative net_import = exporting
