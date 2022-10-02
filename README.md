Here upload for 3 website
+ file.io
+ zippyshare.com
+ anonfiles.com

#### Usage (CLI)
````
usage: main.py [-h] [-f] [-s] [-l]

		Uploader
    Author © github.com/motebaya 2022

options:
  -h, --help         show this help message and exit
  -f , --file        input your file
  -s , --server      chosee server, type --list for show all server
  -l, --list-server  display all server list .eg zippyshare .etc

example: 
./main.py -f yourfile -s anonfiles
````

loader get it from [here](https://stackoverflow.com/questions/22029562/python-how-to-make-simple-animated-loading-while-process-is-running)  
i don't know how to add progress uploader bar with tqdm  
for some website like httpbin its posible,  
but in this case some site like zippyshare have multipart form data  
for upload it, see in [this](https://stackoverflow.com/a/13911048/18108149) requests not support with stream upload,  
also i trying with [requests_toolbelt](https://pypi.org/project/requests-toolbelt/) but not working with [asyncio](https://docs.python.org/3/library/asyncio.html)  
