import argparse


def cli():
    parser = argparse.ArgumentParser()

    parser.add_argument('command', type=str, help='command to execute')
    parser.add_argument('--hg', type=str,
                        help='hypergraph db', default='gb.hg')

    args = parser.parse_args()

    print('command: {}'.format(args.command))
    if args.hg:
        print('hypergraph: {}'.format(args.hg))

    print()

    if args.command == 'run':
        pass
    else:
        print('unknown command: {}'.format(args.command))
