from scrapy.exporters import BaseItemExporter
from itemadapter import ItemAdapter
from scrapy.utils.python import to_unicode
import xlwt


class ExcelItemExporter(BaseItemExporter):
    def __init__(self, file, **kwargs):
        self._configure(kwargs)

        if not self.encoding:
            self.encoding = 'utf-8'

        self.file = file
        self.wbook = xlwt.Workbook()
        self.wsheet = self.wbook.add_sheet('scrapy')
        self._headers_not_written = True
        self.row = 0

    def _write_headers_and_set_fields_to_export(self, item):
        if not self.fields_to_export:
            # use declared field names, or keys if the item is a dict
            self.fields_to_export = ItemAdapter(item).field_names()

        headers = list(self._build_row(self.fields_to_export))
        for col, header in enumerate(headers):
            self.wsheet.write(self.row, col, header)

        self.row += 1

    def finish_exporting(self):
        self.wbook.save(self.file)

    def export_item(self, item):
        if self._headers_not_written:
            self._headers_not_written = False
            self._write_headers_and_set_fields_to_export(item)

        fields = self._get_serialized_fields(item)

        for col, v in enumerate(x for _, x in fields):
            self.wsheet.write(self.row, col, v)

        self.row += 1

    def _build_row(self, values):
        for s in values:
            try:
                yield to_unicode(s, self.encoding)
            except TypeError:
                yield s
