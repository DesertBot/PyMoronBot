"""
Created on Jul 31, 2013

@author: StarlitGhost, Emily
"""
from bs4 import BeautifulSoup
from twisted.plugin import IPlugin
from zope.interface import implementer

from desertbot.message import IRCMessage
from desertbot.moduleinterface import IModule
from desertbot.modules.commandinterface import BotCommand
from desertbot.response import IRCResponse


@implementer(IPlugin, IModule)
class Dinner(BotCommand):
    def triggers(self):
        return ['dinner']

    def help(self, query):
        return ('dinner (meat/veg/drink) - asks WhatTheFuckShouldIMakeForDinner.com'
                ' what you should make for dinner')

    def execute(self, message: IRCMessage):
        wtfsimfd = "http://whatthefuckshouldimakefordinner.com/{}"

        options = {'meat': 'index.php', 'veg': 'veg.php', 'drink': 'drinks.php'}

        option = 'meat'
        if len(message.parameterList) > 0:
            option = message.parameterList[0]

        if option in options:
            response = self.bot.moduleHandler.runActionUntilValue('fetch-url',
                                                                  wtfsimfd.format(options[option]))

            soup = BeautifulSoup(response.content, 'lxml')

            phrase = soup.find('dl').text.strip()
            item = soup.find('a')
            link = self.bot.moduleHandler.runActionUntilValue('shorten-url', item['href'])
            item = item.text.strip()

            return IRCResponse("{}... {} {}".format(phrase, item, link), message.replyTo)

        else:
            error = ("'{}' is not a recognized dinner type, please choose one of {}"
                     .format(option, '/'.join(options.keys())))
            return IRCResponse(error, message.replyTo)


dinner = Dinner()
