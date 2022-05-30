import scrapy
import pandas as pd

class DecksSpider(scrapy.Spider):
    name = 'decks'

    def start_requests(self):
      mtg_formats = [
      'modern',
      'standard',
      'legacy'
      ]

      for mtg_format in mtg_formats:
          yield scrapy.Request(url=f'https://www.mtggoldfish.com/metagame/{mtg_format}/full', callback=self.parse, cb_kwargs=dict(mtg_format=mtg_format))

    def parse(self, response, mtg_format):
      decks = dict()
      id_deck = 0

      for deck in response.css('div.archetype-tile'):
        try:
          colors = deck.css("span.manacost::attr(aria-label)").get()[8:].split(' ')
        except TypeError:
          colors = []

        no_decks = deck.css('span.archetype-tile-statistic-value-extra-data::text').get().strip()

        decks[id_deck] = {
          'name': deck.css('span.deck-price-paper').css('a::text').get(),
          'link': f'https://www.mtggoldfish.com{deck.css("span.deck-price-paper").css("a").attrib["href"]}',
          'color_id': colors,
          'percent_of_meta': deck.css('div.archetype-tile-statistic-value::text').get().strip(),
          'no_of_decks': no_decks[1:len(no_decks)]
        }

        id_deck += 1
      
      data = pd.DataFrame.from_dict(decks, orient='index')
      data.to_csv(f'decks-{mtg_format}.csv')