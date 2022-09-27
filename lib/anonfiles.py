#!/usr/bin/env python3

from . import Base

class Anonfiles(Base):
    host = 'https://{}.anonfiles.com/'
    async def upload(self, fname):
        res = await self.post(
            "{}upload".format(self.host.format('api')), files={
                'file': (
                    fname, open(fname, 'rb'), self.get_mime(fname)
                )}
            )
        res = res.json()
        if res['status']:
            l = res['data']['file']['url']
            return dict(
                status=True,
                short=l['short'],
                full=l['full']
            )
        return False