from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Owner(models.Model):
    _name = "owner"
    _description = "Property Owner"
    _rec_name = "owner_name"
    owner_name = fields.Char(required=True, default="Mohamed")
    owner_phone = fields.Char(required=True)
    owner_address = fields.Char()
    property_ids = fields.One2many('property' , 'owner_id')
    _sql_constraints = [
        ('unique_name' , 'unique("owner_name")' , 'Owner Name is already Exist')
    ]
    
    @api.constrains('owner_name')
    def _check_name_length(self):
        for rec in self:
            if rec.owner_name and len(rec.owner_name) > 12:
                raise ValidationError("Owner name cannot exceed 12 characters.")
            
    
