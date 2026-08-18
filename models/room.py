from odoo import models , fields , api
class Room(models.Model):
    _name = 'room'
    _description = 'Room model'
    
    property_id = fields.Many2one('property' , required=True , ondelete = 'cascade')
    room_name = fields.Char(required=True)
    width = fields.Float()
    height = fields.Float()
    
    area = fields.Float(compute='_compute_area' , store=True)
    
    
    @api.depends('width' , 'height')
    def _compute_area(self):
        for rec in self:
            rec.area = rec.width * rec.height