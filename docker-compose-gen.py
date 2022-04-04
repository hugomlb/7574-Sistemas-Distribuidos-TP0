import argparse

def open_file():
  try:
    file = open("docker-compose-dev.yaml", "w")
  except IOError:
    print("I/O Error")
    sys.exit(1)
  except FileNotFoundError:
    print("File not found Error", end='')
  return file

def generate_docker_compose(f, clients):

  f.write(
"""
version: '3'
services:
  server:
    container_name: server
    image: server:latest
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
      - SERVER_PORT=12345
      - SERVER_LISTEN_BACKLOG=7
      - LOGGING_LEVEL=DEBUG
    networks:
      - testing_net
"""
    )
  for i in range(1, clients +1):
    f.write(
"""
  client{id}:
    container_name: client{id}
    image: client:latest
    entrypoint: /client
    environment:
      - CLI_ID={id}
      - CLI_SERVER_ADDRESS=server:12345
      - CLI_LOOP_LAPSE=1m2s
      - CLI_LOG_LEVEL=DEBUG
    networks:
      - testing_net
    depends_on:
      - server
""".format(id = i)    
  )
  f.write(
"""
networks:
  testing_net:
    ipam:
      driver: default
      config:
        - subnet: 172.25.125.0/24
"""    
  )


def parse_args():
  usage = "[-h] [-c clients]"
  description = "Generates the file docker-compose-dev.yaml with c clients"

  parser = argparse.ArgumentParser("./main.py",
    usage='%(prog)s {}\n\n{}'.format(usage, description))

  group = parser.add_mutually_exclusive_group()
  group.add_argument("-c", "--clients", default=2, type=int, const=2, nargs='?',
    help="Number of clients to add to docker-compose")

  return parser.parse_args()
    
def run():
  args = parse_args()
  file = open_file()
  generate_docker_compose(file, args.clients)
  file.close()

if __name__ == "__main__":
    run()