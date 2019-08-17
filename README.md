# asyncproxy
#### Install
```bash
cd ~
git clone https://github.com/SlavikMIPT/tgasyncproxy.git
cd tgasyncproxy
pip3 install -r requirements.txt
```
#### Server
- `--size` - max queue size
- `--rps` - requests per second
- `--host` - host address
- `--port` - port address
```bash
python3 async_proxy.py --size 1000 --host 127.0.0.1 --port 8081
```
#### Client
- `--id` - chat id
- `--url` - api url
- `--token` - bot token
- `--rps` - requests per second
```bash
python3 examples/client_flood.py --id 1234567 --url http://127.0.0.1:8081 --token 1234567:xxxxxxxxx --rps 100
```
#### HTTPS
Use nginx proxy