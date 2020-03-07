import argparse
import gbserver.server as server


HG = None


def cli():
    parser = argparse.ArgumentParser()

    parser.add_argument('command', type=str, help='command to execute')
    parser.add_argument('--hg', type=str,
                        help='hypergraph db', default='gb.hg')
    parser.add_argument('--host', type=str, help='host', default='localhost')
    parser.add_argument('--port', type=int, help='port', default=5000)

    args = parser.parse_args()

    print('command: {}'.format(args.command))
    global HG
    HG = args.hg
    print('hypergraph: {}'.format(HG))

    print()

    if args.command == 'run':
        server.app.config.from_object(__name__)
        server.app.run(host=args.host, port=args.port)
    else:
        print('unknown command: {}'.format(args.command))
