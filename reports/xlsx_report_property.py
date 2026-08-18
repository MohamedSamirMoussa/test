from odoo import http
from odoo.http import request
from ast import literal_eval
import io
import xlsxwriter


class XlsxPropertyReport(http.Controller):
    
    
    @http.route(
        "/property/excel/report/<string:property_ids>",
        type="http",
        auth="user"
        )
    def download_property_excel_sheet(self , property_ids):
        property_ids = request.env['property'].browse(literal_eval(property_ids))
        print(property_ids)
        output = io.BytesIO()
        
        workbook = xlsxwriter.Workbook(
            output,
            {'in_memory':True}
        )
        worksheet= workbook.add_worksheet('Properties')
        header_format = workbook.add_format({'bold':True, 'bg_color':'#D3D3D3' , 'border':1 , 'align':'center'})
        row_format = workbook.add_format({'border':1 , 'align':'center'})
        
        headers = ['Name' , 'Postcode' , 'Selling Price' ,'Garden' , 'Garage', 'Total Area' ]
        for col_num, header in enumerate(headers):
            worksheet.write(0 , col_num , header , header_format)
         
        row_num = 1   
        for property_id in property_ids:
            worksheet.write(row_num , 0 , property_id.name , row_format)    
            worksheet.write(row_num , 1 , property_id.post_code , row_format)    
            worksheet.write(row_num , 2 , property_id.selling_price , row_format)    
            worksheet.write(row_num , 3 , property_id.garden , row_format)    
            worksheet.write(row_num , 4 , property_id.garage , row_format)    
            worksheet.write(row_num , 5 , property_id.total_area , row_format)    
            row_nom += 1
        workbook.close()
        output.seek(0)
        
        filename = 'Property Lead.xlsx'
        
        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreedsheetml.sheet'),
                ('Content-Disposition' , f'attachment; filename = {filename}'),
            ]
        )
        