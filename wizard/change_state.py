from odoo import models , fields
from odoo.exceptions import UserError

class ChangeState(models.TransientModel):
    _name = "change.state"
    
    property_id = fields.Many2one("property")
    state = fields.Selection([
        ("draft" , "Draft"),
        ("pending" , "Pending"),
    ] , default="draft")
    
    reason = fields.Text()
    
    
    def action_confirm(self):
        if self.property_id.state != "closed":
            raise UserError(f"You can't change {self.state}")
        
        
        self.property_id.state = self.state
        self.property_id.create_history_rec('closed' , self.state , self.reason)
        