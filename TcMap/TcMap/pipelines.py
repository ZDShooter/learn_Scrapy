# -*- coding: utf-8 -*-

# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from traceback import print_tb


class TcmapPipeline(object):
    def process_item(self, item, spider):
        # 转换为字典格式
        items = dict(item)
        # 获取区域代码、名称以及简介
        area_code = items['fileCode']
        area_name = items['fileName']
        area_profile = tuple(items['fileContent'])
        # 创建文件
        my_file = open('Files/%s_%s.txt' % (area_code, area_name), 'w')
        # 处理文本信息格式,将文本出路过程的错误记录到log.txt.
        # 由于爬去数据不规整,如果使用str.join()函数,会导致格式不整齐.
        try:
            for paragraph in area_profile:
                content = ''
                if paragraph:
                    for para in paragraph.split():
                        if para:
                            content += para
                        else:
                            pass
                    paragraph = content
                    if paragraph:
                        my_file.write(" "*4 + '%s' % paragraph + "\n")
                    else:
                        pass
                else:
                    pass
        except Exception as ex:
            file_log = open('TcMap/log.txt', 'a')
            print(ex, file=file_log)
            print_tb(ex.__traceback__, file=file_log)
            file_log.close()
        # 关闭文件
        my_file.close()
        # 此处换成yield不生成文件
        return item
