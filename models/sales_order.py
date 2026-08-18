from odoo import models , fields

class SalesOrder(models.Model):
    _inherit = 'sale.order'
    
    property_id = fields.Many2one("property" , string="Property")
    
    def action_confirm(self):
        res = super(SalesOrder , self).action_confirm()
        
        print("Hello, World!")
        return res 
        
    
    
    
    
    