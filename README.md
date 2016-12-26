# twantalyzin
Twitter Analysis

Get a live stream of tweets relating to the specified terms-to-track, and format as csv for analysis. 

To use:  
* Create a Twitter developers account  
* Create a local_config.py with keys:
     
        cons_tok = ""  
        cons_sec = ""  
        app_tok = ""  
        app_sec = ""  
        CONNECTION_STRING = "sqlite:///twantalyzin.db"  
        
* Update keys with token and secret from your personal Twitter developer account  
* Update settings.py with your terms to track  

* Run twit_analysis.py  

* Run dump.py  
