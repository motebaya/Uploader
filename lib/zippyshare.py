#!/usr/bin/env python3

from importlib.metadata import files
from . import Base
import re

class Zippyshare(Base):
    host = "https://www{}.zippyshare.com/"
    async def get_server(self):
        server = await self.get(self.host.replace("{}", ""))
        if (server := re.search(r"(?:var\sserver\s=\s'www(\d{1,3}))", server.text)):
            return server.group(1)
        return False
    
    async def upload(self, fname):
        if (server := await self.get_server()):
            res = await self.post(
                self.host.format(server) + "upload", data={
                    "name": fname,
                    "notprivate": True,
                    "zipname": "",
                    "ziphash": "",
                    "embPlayerValues": False
                }, files={
                    "file": (fname, open(fname, "rb"), self.get_mime(fname))
                }
            )
            return {
                'status': True,
                'page': self.parse(res.text)
            }
        return self.failed
            # open("response.html", "w").write(res.text)
            # print(res.text)
    
    async def extract_links(self, soup):
        if (m := soup.find('ul', class_='menu').find_all("li")):
            if (v := soup.find(class_='clear').parent.find_all('div')):
                if (any(text := list(map(lambda i: i.textarea.text.strip().splitlines(), v)))):
                    return {"status": True, **dict(zip(
                        map(
                            (lambda x: re.sub(
                                r"[\W]+", " ", x.text.strip(
                            ).title(
                        ))),m),
                        map(
                            (lambda i: i[0] if len(i
                                ) != 2 else ' '.join(i) if len(i
                            ) != 0 else None),
                        text)
                    ))}
                return self.failed
            return self.failed
        return self.failed
                