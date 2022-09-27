#!/usr/bin/python

from . import Base

class Fileio(Base):
    host = "https://file.io/"
    async def upload(self, fname):
        res = await self.post(f"{self.host}?title={fname}", files={
            "file": (
                fname, open(fname, "rb"), self.get_mime(fname)
            )
        })
        res = res.json()
        if res["success"]:
            return dict(
                status=res['success'],
                url=res['link'],
                limit=str(res['maxDownloads']),
                expire=self.validDate(res['expires']),
                created=self.validDate(res['created'])
            )
        return self.failed