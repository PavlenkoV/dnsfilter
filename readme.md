# dnsfilter

####It's simple DNS proxy filter server with configurable blacklist based on twisted framework for study projects (NOT for production).

#####Requirements  
python2 (version 2.7) and twisted (version 16.5.0)  
It's strongly recommended to install inside isolated virtual environment!  
More details http://docs.python-guide.org/en/latest/dev/virtualenvs/.  
You need root to start dnsfilter on TCP/UDP port 53 (default setting for dnsfilter).  

#####Initial Setup:  
you can check if port 53 is free by:  
1) run check_port.py (you need root to execute it), f.e  
```bash
    $ sudo python2 check_port.py  
```
2)  
```bash
    $ sudo lsof -i:53  
```
Usually, system service/dns server uses it.  
In my scenario, in Ubuntu systemd-resolved and dnsmasq server is on port 53.  
To disbale it:  
1)  
```bash
    $ sudo service systemd-resolved stop  
```
2) edit /etc/NetworkManager/NetworkManager.conf and comment out the line dns=dnsmasq to have line, like:  
```
    #dns=dnsmasq  
```
restart Network-Manager  
```bash
    $ sudo restart network-manager  
```
or  
```bash
    $ sudo service network-manager restart  
```
You can start web - server to get html page with specified answer if it's query for restricted domain names (you can edit this page in json.conf):
You can use any web-server, but you need root to start it on port 80.
1) F.e, default python http-server (index.html and stop_page.jpg should be in same folder you start server)  
```
    $ sudo python -m http.server 80
```  
2) or twisted web - server (if you using virtual environment you should indicate path to twisted)  
```
    $ sudo /home/username/path/to/virtual_env/bin/twistd web --port tcp:80 --path=.
```  
it will start twisted server, which is at /home/username/path/to/virtual_env/bin/twistd and will use current folder as root for server.  

######Editing json.conf  
Create blacklist:  
You can add restricted domain names in json.conf , like 'name1, 'name2' etc, separated by comma:  
```
    "blacklist":["vk.com", "odnoklassniki.ru"]  
```
You can also specified:  
  * specify DNS servers for response if query is not restricted  
Google DNS servers are default.
  * starting/disabling logs for all queries or restricted only  
Please be careful if you are using logging for all queries due to big amount of data
  * different options for index.html

#####Run dnsfilter:
```
    $ sudo /home/username/path/to/virtual_env/bin/python dnsfilter.py
```  

#####Running test:
'127.0.0.1' is default address for restricted queries.  
You can check if all restricted queries from <mark>blacklist</mark> is redirected to it.  
```
    $ python test.py
```



