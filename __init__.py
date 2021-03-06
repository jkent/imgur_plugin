# -*- coding: utf-8 -*-
# vim: set ts=4 et

import re

from imgurpython import ImgurClient

from plugin import *


imgur_re = re.compile(
  'imgur.com/(?:gallery/|r/(?P<subreddit>\\w+)/)?'  +
  '(?P<id>\\w+)(?P<extension>\\.\\w+)?'
)


class Plugin(BasePlugin):
    @hook('imgur.com')
    @hook('i.imgur.com')
    @hook('m.imgur.com')
    def imgur_url(self, msg, domain, url):
        m = imgur_re.search(url)
        if not m:
            return

        client_id = self.bot.config.get('imgur', 'client_id')
        client_secret = self.bot.config('imgur', 'client_secret')

        client = ImgurClient(client_id, client_secret)

        if m.group('subreddit'):
            item = client.subreddit_image(m.group('subreddit'), m.group('id'))
        else:
            try:
                item = client.gallery_item(m.group('id'))
            except:
                item = client.get_image(m.group('id'))

        item_type = 'Album' if getattr(item, 'is_album', False) else 'Image'
        item_type = 'NSFW ' + item_type if item.nsfw else item_type

        if item.title:
            msg.reply('%s: %s (%d)' % (item_type, item.title,
                                       getattr(item, 'score', -1)))
        else:
            msg.reply('%s: Untitled' % item_type)

        if m.group('extension'):
            msg.reply('Gallery link: http://imgur.com/%s' % item.id)
