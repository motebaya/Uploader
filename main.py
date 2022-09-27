#!/usr/bin/python

# Time: Tue Sep 27 08:20:02 2022
# free code guys
from lib import Base, basename, Loader
import asyncio, argparse

uploader = {obj.__name__.lower(): obj for obj in Base.__subclasses__() if obj}
keys = list(uploader.keys())
credits = "\n\t\tUploader\n    Author \u00A9 github.com/motebaya 2022\n"

class Main(Base):
    async def _main(self, fname, server):
        global uploader
        print(credits)
        if (fullpath := self.check_file(fname)):
            if (filesize := self.check_size(fullpath)):
                print(
                    f" [{server}] Filename: {basename(fullpath)}\n"
                    f" [{server}] Filesize: {self.format_size(filesize)}"
                )
                loading = Loader(f'Uploading {fname}...').start()
                res = await uploader[server]().upload(fname)
                loading.stop()
                if res['status']:
                    if (server == 'zippyshare'):
                        loading = Loader('Extracting Lins..').start()
                        res = await uploader[server]().extract_links(res['page'])
                        loading.stop()
                    for k, v in list(res.items())[1:]:
                        print(
                            f" [{server}] {k.title()}: {v}"
                        )
                else:
                    exit(res)
            else:
                raise ValueError(
                    'File size to big!'
                )
        else:
            raise FileNotFoundError(
                f" {fname} not found !"
            )

if __name__=='__main__':
    parser = argparse.ArgumentParser(
        description=credits,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-f', '--file', metavar='', type=str, help='input your file')
    parser.add_argument('-s', '--server', metavar='', help='chosee server, type --list for show all server')
    parser.add_argument('-l', '--list-server', help='display all server list .eg zippyshare .etc', action='store_true')
    arg = parser.parse_args()
    if arg.list_server:
        print()
        for i, e in enumerate(keys, 1):
            print(
                f" {i}. {e.title()} [{uploader[e].host}]"
            )
    elif arg.file and arg.server:
        if arg.server.lower() in keys:
            asyncio.run(
                Main()._main(
                    arg.file, arg.server.lower()
                )
            )
        else:
            exit(
                f" {arg.server} not found , type --help for usage!"
            )
    else:
        parser.print_help()

# print(arg)
# print(list(uploader.keys()))

# parser.print_help()