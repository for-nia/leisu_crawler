# coding=utf8
import scrapy
import re
from leisu_crawler.items.Match import Match

NAME='LeisuLiveMatchers'
class LeisuLiveMatches(scrapy.Spider):
    name = NAME

    fenxi='https://live.leisu.com/shujufenxi-{}/'
    shypeilv='https://live.leisu.com/3in1-{}/'
    oupei='https://live.leisu.com/oupei-{}'
    yapei='https://live.leisu.com/yapan-{}'
    daxiao='https://live.leisu.com/daxiaoqiu-{}'
    statistic_url='https://live.leisu.com/detail-{}'

    def start_requests(self):
        urls=['http://live.leisu.com/']
        yield scrapy.Request(urls[0],callback=self.parse)

    def parse(self,response):
        games=response.css('.list-item')
        for game in games:
            match_id=game.xpath('.//@data-id').extract()[0]
            yield scrapy.Request(self.fenxi.format(match_id),callback=self.parse_fenxi)
            yield scrapy.Request(self.shypeilv.format(match_id),callback=self.parse_peilv)
            yield scrapy.Request(self.yapei.format(match_id),callback=self.parse_yapei)
            yield scrapy.Request(self.statistic_url.format(match_id,callback=self.statistic))
            yield scrapy.Request(self.daxiao.format(match_id),callback=self.parse_daxiao)
            yield scrapy.Request(self.oupei.format(match_id),callback=self.parse_oupei)

    def parse_fenxi(self, response):
        match_id = int(re.compile(r'https://live.leisu.com/shujufenxi-(\d+)').match(response.url).group(1))
        home = response.css('.vs-l')[0]
        home_team_name = home.xpath('.//div/h1/text()').extract()[0]
        home_head = 'http:' + home.xpath('.//i/@style').re(r'background-image: url\((.*)\)')[0]
        away = response.css('.vs-r')[0]
        away_team_name = home.xpath('.//div/h1/text()').extract()[0]
        away_head = 'http:' + away.xpath('.//i/@style').re(r'background-image: url\((.*)\)')[0]
        begin_time = response.xpath('//div[@class="page-info"]/p/span/text()')
        match=Match(match_id=match_id,home_name=home_team_name,home_head=home_head,away_name=away_team_name,away_head=away_head,begin_time=begin_time.extract()[0] + ' ' + begin_time.extract()[1] + ':00')
        match.save()
        #print begin_time.extract()[0] + ' ' + begin_time.extract()[1] + ':00'
        #print 'homeName:%s,head:%s---awaysName:%s,head:%s' % (home_team_name, home_head, away_team_name, away_head)


    def get_shy_list(self,tr):
        first=tr.xpath('.//td/span/text()').extract()
        yield first[0] if len(first)>0 else None
        second=tr.xpath('.//td/text()').extract()
        yield second[0] if len(second)>0 else None
        third = tr.xpath('.//td/span/text()').extract()
        yield third[0] if len(third)>0 else None

    def parse_peilv(self,response):
        trs = response.xpath('//table[@class="main"]/tbody/tr')
        for tr in trs:
            company = tr.xpath('.//@data-company').extract()[0]
            print company
            rangqiu = tr.xpath('.//td[@class="rangQiu"]/table/tbody/tr')[0]
            rq_first = [x for x in self.get_shy_list(rangqiu)]
            rq_current = [x for x in self.get_shy_list(rangqiu)]
            bzp = tr.xpath('.//td[@class="biaoZhunPan"]/table/tbody/tr')[0]
            bzp_first= [x for x in self.get_shy_list(bzp)]
            bzp_current = [x for x in self.get_shy_list(bzp)]
            print bzp_first+bzp_current
            dxq_rate = tr.xpath('.//td[contains(@class,"daXiaoQiu")]/table/tbody/tr')
            dxq_first = [x for x in self.get_shy_list(dxq_rate)]
            dxq_current = [x for x in self.get_shy_list(dxq_rate)]
            print dxq_first+dxq_current


    def parse_oupei(self,response):
        trs=response.xpath('//table[@class="main"]/tbody/tr')
        for tr in trs:
            company = tr.xpath('.//@data-company').extract()[0]
            print company
            peilv = tr.xpath('.//td[@class="peilv"]/table/tbody/tr')
            peilv_first=[x for x in peilv[0].xpath('.//td/span/text()').extract()]
            peilv_current=[x for x in peilv[1].xpath('.//td/span/text()').extract()]
            gailv = tr.xpath('.//td[@class="gailv"]/table/tbody/tr')
            gailv_first = gailv[0].xpath('.//@data-rate').extract()[0]
            gailv_current = gailv[1].xpath('.//@data-rate').extract()[0]
            print eval(gailv_first)+eval(gailv_current)
            fanhuan = tr.xpath('.//td[contains(@class,"fanhuan")]/@data-rate').extract()[0]
            kelly_rate= tr.xpath('.//td[contains(@class,"kelly")]/table/tbody/tr')
            kelly_first=[x for x in kelly_rate[0].xpath('.//td/span/text()').extract()]
            kelly_current=[x for x in kelly_rate[1].xpath('.//td/span/text()').extract()]
            print kelly_first+kelly_current


    def parse_yapei(self,response):
        trs = response.xpath('//table[@class="main"]/tbody/tr')
        for tr in trs:
            company = tr.xpath('.//@data-company').extract()[0]
            data_odds = tr.xpath('.//@data-odds').extract()[0]
            time = tr.xpath('.//td[@class="time"]/text()').extract()[0]
            print company + data_odds + time

    def statistic(self,response):
        pass

    def parse_daxiao(self,response):
        trs=response.xpath('//table[@class="main"]/tbody/tr')
        for tr in trs:
            company=tr.xpath('.//@data-company').extract()[0]
            data_odds=tr.xpath('.//@data-odds').extract()[0]
            time=tr.xpath('.//td[@class="time"]/text()').extract()[0]
            print company+data_odds+time
