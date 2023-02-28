First, set your browser's proxy settings to localhost and port 50008. Next, open a terminal to this directory and run

python3 web_proxy.py

Your browser should now be able to utilize this web proxy. WARNING: Some sites might not save to the cache when an error leads to a "last-modified" header not appearing. These sites will still load, though, tested as of 2/27/2023